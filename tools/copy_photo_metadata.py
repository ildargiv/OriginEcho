# -*- coding: utf-8 -*-
"""
Копирование всех данных (EXIF) с оригинальной фотографии на обработанную ИИ.

Дополнительно умеет:
  * привести формат обработанного фото к формату оригинала;
  * переименовать результат: "<имя оригинала> <имя копии>.<расширение оригинала>".

Режимы:
  1) Двойной клик по "Копировать данные фото.bat" -> окно программы.
  2) Командная строка:
     python tools/copy_photo_metadata.py оригинал.jpg обработанное.jpg [ещё.jpg ...]
     python tools/copy_photo_metadata.py --folder ПАПКА_ОРИГИНАЛОВ ПАПКА_ОБРАБОТАННЫХ
"""
import os
import shutil
import subprocess
import sys

from PIL import Image
from i18n import tm

Image.MAX_IMAGE_PIXELS = None

try:  # поддержка HEIC (iPhone), если установлен pillow-heif
    import pillow_heif  # type: ignore
    pillow_heif.register_heif_opener()
except Exception:
    pass

# Форматы, в которые умеем ПИСАТЬ (вместе с расширением)
WRITABLE = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG",
            ".webp": "WEBP", ".tif": "TIFF", ".tiff": "TIFF"}
IMG_EXT = set(WRITABLE) | {".heic", ".cr2", ".cr3", ".arw", ".nef", ".dng"}

# ----------------------------------------------------------------------
# Необязательный exiftool: копирует ВСЁ, включая XMP и IPTC


def find_exiftool():
    """Ищет exiftool.exe: в папках проекта, рядом и в PATH."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # корень проекта
    here = os.path.dirname(os.path.abspath(__file__))
    for base in (root, here):
        for dirpath, _, files in os.walk(base):
            if os.path.basename(dirpath).startswith(".git"):
                continue
            for f in files:
                if f.lower() == "exiftool.exe":
                    return os.path.join(dirpath, f)
    return shutil.which("exiftool")


def exiftool_copy(src, dst):
    """Копирует весь набор метаданных утилитой exiftool (EXIF+IPTC+XMP+ICC)."""
    exe = find_exiftool()
    if not exe:
        return False, "exiftool не найден"
    try:
        r = subprocess.run(
            [exe, "-q", "-q", "-overwrite_original",
             "-tagsFromFile", src, "-all:all", "-P", dst],
            capture_output=True, timeout=120)
        return r.returncode == 0, (r.stderr or r.stdout or b"").decode("utf-8", "replace")
    except Exception as e:
        return False, str(e)



# ----------------------------------------------------------------------
# Извлечение "сырых" блоков из файла-источника


def raw_exif(path):
    with Image.open(path) as im:
        return im.info.get("exif")  # bytes с заголовком b"Exif\x00\x00"


def raw_icc(path):
    with Image.open(path) as im:
        return im.info.get("icc_profile")


def src_blocks(src):
    """EXIF и ICC из источника."""
    return raw_exif(src) or None, raw_icc(src) or None


def write_jpeg_with_meta(read_path, out_path, exif_payload=None,
                         icc_payload=None):
    """Переписывает JPEG (читает read_path, пишет в out_path),
    заменив EXIF и ICC, не трогая ни байта данных картинки."""
    with open(read_path, "rb") as f:
        d = f.read()
    if d[:2] != b"\xff\xd8":
        raise ValueError("не JPEG")

    # диапазоны старых сегментов, которые заменяем
    drop = []
    pos = 2
    while pos < len(d):
        if d[pos] != 0xFF:
            break
        m = d[pos + 1]
        if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7 or m == 0x01:
            pos += 2
            continue
        ln = int.from_bytes(d[pos + 2:pos + 4], "big")
        payload = d[pos + 4:pos + 2 + ln]
        if m == 0xE1 and payload.startswith(b"Exif\x00\x00"):
            drop.append((pos, pos + 2 + ln))
        elif m == 0xE2 and payload.startswith(b"ICC_PROFILE\x00"):
            drop.append((pos, pos + 2 + ln))
        pos += 2 + ln

    # позиция вставки: сразу после ведущих APP0 (JFIF) — как пишет сам обозреватель
    pos, ins = 2, 2
    while True:
        if d[pos:pos + 2] != b"\xff\xe0":
            break
        ln = int.from_bytes(d[pos + 2:pos + 4], "big")
        pos += 2 + ln
        ins = pos

    newseg = b""
    for marker, payload in ((b"\xff\xe1", exif_payload),
                            (b"\xff\xe2", icc_payload)):
        if payload:
            # длина сегмента включает 2 байта самого поля длины
            newseg += marker + (len(payload) + 2).to_bytes(2, "big") + payload

    buf = bytearray(d[:ins] + newseg)
    prev = ins
    for a, b in sorted(drop):
        if b <= ins:
            continue
        buf += d[prev:a]
        prev = b
    buf += d[prev:]

    with open(out_path, "wb") as f:
        f.write(buf)


def save_params(fmt):
    if fmt == "JPEG":
        return {"quality": 95, "subsampling": 0}
    if fmt == "WEBP":
        return {"quality": 95}
    if fmt == "PNG":
        return {"optimize": True}
    return {}


# ----------------------------------------------------------------------
# Даты файлов (создан / изменён) — как у оригинала


def copy_file_times(src, dst):
    st = os.stat(src)
    mtime = st.st_mtime
    os.utime(dst, (mtime, mtime))  # дата изменения

    try:  # дата создания на Windows (нужен pywin32)
        import win32file
        import pywintypes
        h = win32file.CreateFile(
            dst, win32file.GENERIC_WRITE,
            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
            None, win32file.OPEN_EXISTING,
            win32file.FILE_ATTRIBUTE_NORMAL, None)
        win32file.SetFileTime(h,
                              pywintypes.Timestamp(st.st_ctime),
                              pywintypes.Timestamp(st.st_atime),
                              pywintypes.Timestamp(st.st_mtime))
        h.Close()
    except Exception:
        pass  # без pywin32 остаётся только дата изменения


# ----------------------------------------------------------------------
# Имя и формат результата


def src_is_jpeg(p):
    return os.path.splitext(p)[1].lower() in (".jpg", ".jpeg")


def make_out_path(src, dst):
    """Новое имя: имя оригинала + пробел + имя копии + расширение оригинала."""
    src_stem = os.path.splitext(os.path.basename(src))[0]
    dst_stem = os.path.splitext(os.path.basename(dst))[0]
    src_ext = os.path.splitext(src)[1].lower()
    if src_ext in WRITABLE:
        ext = src_ext
    else:  # оригинал в формате, который мы не пишем (HEIC и т.п.) — оставляем расширение копии
        ext = os.path.splitext(dst)[1].lower() or ".jpg"
    if src_stem.lower() == dst_stem.lower():
        name = src_stem + ext
    else:
        name = f"{src_stem} {dst_stem}{ext}"
    out = os.path.join(os.path.dirname(dst) or ".", name)
    # не даём перезаписать соседние файлы с таким же именем
    n = 1
    while os.path.exists(out) and os.path.abspath(out) != os.path.abspath(dst):
        stem, e = os.path.splitext(name)
        n += 1
        out = os.path.join(os.path.dirname(dst) or ".",
                           f"{stem} ({n}){e}")
    return out


# ----------------------------------------------------------------------
# Основная операция


def process_pair(src, dst, copy_icc=True, copy_dates=True,
                 to_src_format=True, rename=True, delete_old=True,
                 lang="ru"):
    if not os.path.isfile(src):
        return (False, f"[!] {tm('e_src', lang)}: {src}")
    if not os.path.isfile(dst):
        return (False, f"[!] {tm('e_dst', lang)}: {dst}")
    if os.path.abspath(src) == os.path.abspath(dst):
        return (False, f"[!] {tm('e_same', lang)}: {dst}")

    src_ext = os.path.splitext(src)[1].lower()
    dst_ext = os.path.splitext(dst)[1].lower()

    # формат результата
    if to_src_format and src_ext in WRITABLE:
        out_fmt, out_ext = WRITABLE[src_ext], src_ext
    else:
        out_fmt = WRITABLE.get(dst_ext) or "JPEG"
        out_ext = dst_ext

    out_path = make_out_path(src, dst) if (rename or to_src_format) else dst

    exif, icc = src_blocks(src)
    icc = icc if copy_icc else None

    changed = os.path.abspath(out_path) != os.path.abspath(dst) or out_fmt != WRITABLE.get(dst_ext)

    wrote = False
    try:
        if out_fmt == "JPEG" and src_is_jpeg(dst):
            # копия уже JPEG — правим байты без потери качества
            write_jpeg_with_meta(dst, out_path, exif, icc)
            wrote = True
        else:
            # иной формат — пересохраняем картинку в нужный формат
            with Image.open(dst) as im:
                im.load()
                # JPEG/WEBP не поддерживают прозрачность — подложим белый фон
                if out_fmt in ("JPEG", "WEBP") and (
                        im.mode in ("RGBA", "LA") or
                        (im.mode == "P" and "transparency" in im.info)):
                    rgba = im.convert("RGBA")
                    bg = Image.new("RGB", rgba.size, (255, 255, 255))
                    bg.paste(rgba, mask=rgba.split()[-1])
                    im = bg
                elif im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                kwargs = {}
                if exif:
                    kwargs["exif"] = exif
                if icc:
                    kwargs["icc_profile"] = icc
                im.save(out_path, format=out_fmt, **save_params(out_fmt), **kwargs)
            wrote = True
    except Exception as e:
        return (False, f"[!] {os.path.basename(dst)}: {e}")

    if not wrote:
        return (False, f"[!] {os.path.basename(dst)}")

    # полный набор (XMP/IPTC и пр.) — утилитой exiftool, если она есть рядом
    full = ""
    okx = exiftool_copy(src, out_path)
    if okx[0]:
        full = " " + tm("ok_xmp", lang)

    if copy_dates:
        copy_file_times(src, out_path)

    # старый обработанный файл после переименования
    note = ""
    if delete_old and changed and os.path.exists(dst):
        try:
            os.remove(dst)
            note = " (" + tm("del_old", lang) + ")"
        except Exception:
            note = " (" + tm("keep_old", lang) + ")"

    ok = bool(raw_exif(out_path))
    tag = tm("ok_exif", lang) if ok else tm("ok_unsup", lang)
    if full:
        tag += full
    detail = f"{os.path.basename(dst)}"
    if changed:
        detail += f" -> {os.path.basename(out_path)} (" \
                  + tm("fmt", lang).format(f=out_fmt) + ")"
    return (ok, f"[OK] {detail}: {tag}{note}")


def collect_pairs(src, dsts, **kw):
    return [process_pair(src, d, **kw) for d in dsts]


def process_folders(src_dir, dst_dir, **kw):
    """Пакетный режим: пара ищется по имени, иначе — по порядку (1 к 1)."""
    srcs = sorted(os.path.join(src_dir, n)
                  for n in os.listdir(src_dir)
                  if os.path.splitext(n)[1].lower() in IMG_EXT)
    dsts = [os.path.join(dst_dir, n) for n in os.listdir(dst_dir)
            if os.path.splitext(n)[1].lower() in IMG_EXT]
    src_map = {os.path.splitext(os.path.basename(s))[0].lower(): s for s in srcs}

    results, used_srcs = [], set()
    unmatched = []
    for d in dsts:
        s = src_map.get(os.path.splitext(os.path.basename(d))[0].lower())
        if s:
            used_srcs.add(s)
            results.append(process_pair(s, d, **kw))
        else:
            unmatched.append(d)
    # оставшиеся цели подселяем к оставшимся оригиналам по порядку
    spare = [s for s in srcs if s not in used_srcs]
    for d, s in zip(unmatched, spare):
        results.append(process_pair(s, d, **kw))
    for d in unmatched[len(spare):]:
        results.append((False, f"[!] {os.path.basename(d)}: {tm('no_pair', kw.get('lang', 'ru'))}"))
    return results


# ----------------------------------------------------------------------
# Командная строка


def run_cli(argv):
    args = [a for a in argv if not a.startswith("-")]
    kw = {
        "copy_icc": "--no-icc" not in argv,
        "copy_dates": "--no-dates" not in argv,
        "to_src_format": "--no-convert" not in argv,
        "rename": "--no-rename" not in argv,
        "delete_old": "--keep-old" not in argv,
    }
    if "--folder" in argv:
        i = argv.index("--folder")
        if len(argv) < i + 3:
            print("Использование: --folder ПАПКА_ОРИГИНАЛОВ ПАПКА_ОБРАБОТАННЫХ")
            return 1
        res = process_folders(argv[i + 1], argv[i + 2], **kw)
    elif len(args) >= 2:
        src, dsts = args[0], args[1:]
        if os.path.isdir(src) and os.path.isdir(dsts[0]):
            res = process_folders(src, dsts[0], **kw)
        else:
            res = collect_pairs(src, dsts, **kw)
    else:
        print(__doc__)
        return 1

    for ok, line in res:
        print(line)
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(run_cli(sys.argv[1:]))
    import gui  # окно открывается при запуске без аргументов
    gui.main()
