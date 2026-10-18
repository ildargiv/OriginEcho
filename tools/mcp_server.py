# -*- coding: utf-8 -*-
"""MCP-сервер OriginEcho (Model Context Protocol, stdio).

Даёт ИИ-агентам штатные инструменты вместо «сырой» командной строки:

    photo_info         — прочитать историю съёмки файла
    restore_metadata   — перенести метаданные с оригинала на обработанное фото
    process_folders    — пакетная обработка двух папок
    supported_formats  — какие форматы поддерживаются
    app_info           — версия и проверка компонентов

Запуск:
    python tools/mcp_server.py      # из исходников
    OriginEcho.exe --mcp            # тот же exe в режиме сервера

Транспорт — stdin/stdout, по одной JSON-строке на сообщение (JSON-RPC 2.0,
ревизия MCP 2024-11-05). Локально: без портов и без сетевого трафика.
"""
import json
import os
import subprocess
import sys

from copy_photo_metadata import (find_exiftool, make_out_path, process_folders,
                                 process_pair)
from version import __version__

SERVER_NAME = "originecho"
PROTOCOL_FALLBACK = "2024-11-05"

# Ключи, которые выдаём для photo_info (в порядке важности)
INFO_KEYS = [
    "Make", "Model", "LensModel", "LensID",
    "DateTimeOriginal", "CreateDate", "ModifyDate",
    "ExposureTime", "FNumber", "ISO", "FocalLength", "FocalLengthIn35mmFormat",
    "ExposureProgram", "MeteringMode", "Flash", "WhiteBalance",
    "GPSLatitude", "GPSLongitude", "GPSAltitude",
    "Artist", "Copyright", "ImageDescription", "Rating", "Software",
    "ImageWidth", "ImageHeight", "Megapixels", "ColorSpace",
    "ICC_Profile:Description", "FileType", "FileSize",
]

FLAGS_DESC = {
    "convert_to_original_format":
        "Convert the edited file to the original's format (e.g. PNG -> JPEG). Default true.",
    "rename_to_original_plus_edited":
        "Rename the result to '<original stem> <edited stem>.<original ext>'. Default true.",
    "delete_pre_rename_file":
        "Delete the edited file after a successful rename. Default true.",
    "copy_file_dates":
        "Apply the original's created/modified timestamps to the result. Default true.",
    "copy_icc":
        "Copy the colour profile (ICC) as well. Default true.",
    "language": "Report language: 'en' (default) or 'ru'.",
}


def _bool_prop(desc):
    return {"type": "boolean", "description": desc}


TOOLS = [
    {
        "name": "photo_info",
        "description": (
            "Read the shooting history (metadata) of a photo file: camera make and "
            "model, date and time, ISO, exposure, lens, GPS, resolution and colour "
            "profile. Read-only; use it to check what an original photo contains "
            "before or after a transfer."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string",
                         "description": "Absolute path to an image file"},
                "language": {"type": "string", "enum": ["en", "ru"]},
            },
            "required": ["path"],
        },
    },
    {
        "name": "restore_metadata",
        "description": (
            "Copy the full shooting history (EXIF, XMP, IPTC, ICC profile) from the "
            "untouched original photo onto the AI-edited photo. By default also "
            "converts the result to the original's format, renames it to "
            "'<original> <edited>.<ext>', removes the pre-rename file and copies the "
            "file dates. JPEG -> JPEG is done at byte level, so the picture keeps "
            "its quality."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "original": {"type": "string",
                             "description": "Absolute path to the untouched original photo"},
                "edited": {"type": "string",
                           "description": "Absolute path to the AI-edited photo"},
                "convert_to_original_format": _bool_prop(FLAGS_DESC["convert_to_original_format"]),
                "rename_to_original_plus_edited": _bool_prop(FLAGS_DESC["rename_to_original_plus_edited"]),
                "delete_pre_rename_file": _bool_prop(FLAGS_DESC["delete_pre_rename_file"]),
                "copy_file_dates": _bool_prop(FLAGS_DESC["copy_file_dates"]),
                "copy_icc": _bool_prop(FLAGS_DESC["copy_icc"]),
                "language": {"type": "string", "enum": ["en", "ru"]},
            },
            "required": ["original", "edited"],
        },
    },
    {
        "name": "process_folders",
        "description": (
            "Batch mode: transfer shooting history for a whole folder. Edited photos "
            "are matched to originals by file name first, then in order. Options are "
            "the same as restore_metadata."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "originals_dir": {"type": "string",
                                  "description": "Folder with untouched original photos"},
                "edited_dir": {"type": "string",
                               "description": "Folder with AI-edited photos"},
                "convert_to_original_format": _bool_prop(FLAGS_DESC["convert_to_original_format"]),
                "rename_to_original_plus_edited": _bool_prop(FLAGS_DESC["rename_to_original_plus_edited"]),
                "delete_pre_rename_file": _bool_prop(FLAGS_DESC["delete_pre_rename_file"]),
                "copy_file_dates": _bool_prop(FLAGS_DESC["copy_file_dates"]),
                "copy_icc": _bool_prop(FLAGS_DESC["copy_icc"]),
                "language": {"type": "string", "enum": ["en", "ru"]},
            },
            "required": ["originals_dir", "edited_dir"],
        },
    },
    {
        "name": "supported_formats",
        "description": "List the image formats OriginEcho can read and write.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "app_info",
        "description": ("OriginEcho version and health check: Python, executable mode "
                        "and whether the bundled exiftool (needed for full XMP/IPTC "
                        "copy) is available."),
        "inputSchema": {"type": "object", "properties": {}},
    },
]


# ----------------------------------------------------------------------
# Инструменты


def _opts(args):
    """Общие ключи process_pair из аргументов инструмента."""
    lang = args.get("language") or "en"
    return {
        "copy_icc": bool(args.get("copy_icc", True)),
        "copy_dates": bool(args.get("copy_file_dates", True)),
        "to_src_format": bool(args.get("convert_to_original_format", True)),
        "rename": bool(args.get("rename_to_original_plus_edited", True)),
        "delete_old": bool(args.get("delete_pre_rename_file", True)),
        "lang": lang,
    }


def tool_photo_info(args):
    path = args.get("path", "")
    if not os.path.isfile(path):
        return False, f"File not found: {path}"

    lines = [f"Path: {path}",
             f"Size on disk: {os.path.getsize(path)} bytes"]

    exe = find_exiftool()
    if exe:
        try:
            r = subprocess.run([exe, "-j", path], capture_output=True, timeout=60)
            data = json.loads(r.stdout.decode("utf-8", "replace") or "[]")
            if data:
                rec = data[0]
                for key in INFO_KEYS:
                    val = rec.get(key)
                    if val not in (None, "", 0, "undef"):
                        lines.append(f"{key}: {val}")
                xmp = [k for k in rec if k.startswith(("XMP:", "IPTC:"))]
                if xmp:
                    lines.append(f"XMP/IPTC fields present: {len(xmp)}")
                return True, "\n".join(lines)
        except Exception as e:
            lines.append(f"(exiftool failed: {e})")

    # запасной путь без exiftool — читаем EXIF через Pillow
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
            lines += [f"ImageWidth: {w}", f"ImageHeight: {h}", f"FileType: {im.format}"]
            ex = im.getexif()
            plain = {271: "Make", 272: "Model", 306: "DateTime"}
            for tag, name in plain.items():
                if ex.get(tag):
                    lines.append(f"{name}: {ex.get(tag)}")
            try:
                sub = ex.get_ifd(0x8769)  # EXIF IFD
                for tag, name in ((33434, "ExposureTime"), (33437, "FNumber"),
                                  (34855, "ISO"), (37386, "FocalLength")):
                    if sub.get(tag) is not None:
                        lines.append(f"{name}: {sub.get(tag)}")
                if sub.get(36867):
                    lines.append(f"DateTimeOriginal: {sub.get(36867)}")
            except Exception:
                pass
            try:
                gps = ex.get_ifd(0x8825)
                if gps:
                    lines.append("GPS: " + ", ".join(f"{k}={v}" for k, v in gps.items()))
            except Exception:
                pass
            lines.append("ICC profile: " + ("present" if im.info.get("icc_profile") else "missing"))
        return True, "\n".join(lines)
    except Exception as e:
        return False, f"Cannot read the file: {e}"


def tool_restore_metadata(args):
    src, dst = args.get("original", ""), args.get("edited", "")
    kw = _opts(args)
    if not os.path.isfile(src):
        return False, f"Original not found: {src}"
    if not os.path.isfile(dst):
        return False, f"Edited photo not found: {dst}"

    expected = make_out_path(src, dst) if (kw["to_src_format"] or kw["rename"]) else dst
    ok, msg = process_pair(src, dst, **kw)
    out = msg
    if os.path.exists(expected):
        out += f"\nResult file: {expected} ({os.path.getsize(expected)} bytes)"
    else:
        out += "\nResult file: (unchanged in place)"
    return ok, out


def tool_process_folders(args):
    src_dir, dst_dir = args.get("originals_dir", ""), args.get("edited_dir", "")
    for label, d in (("originals_dir", src_dir), ("edited_dir", dst_dir)):
        if not os.path.isdir(d):
            return False, f"{label} is not a folder: {d}"
    kw = _opts(args)
    results = process_folders(src_dir, dst_dir, **kw)
    ok = all(r[0] for r in results)
    text = "\n".join(r[1] for r in results)
    return ok, f"{sum(1 for r in results if r[0])}/{len(results)} photos processed\n{text}"


def tool_supported_formats(args):
    from copy_photo_metadata import IMG_EXT, WRITABLE
    return True, ("Formats OriginEcho writes: " + ", ".join(sorted(WRITABLE)) +
                  "\nFormats it also reads (as originals): " +
                  ", ".join(sorted(set(IMG_EXT) - set(WRITABLE))))


def tool_app_info(args):
    exe = find_exiftool()
    frozen = bool(getattr(sys, "frozen", False))
    return True, "\n".join([
        f"OriginEcho version: {__version__}",
        f"Python: {sys.version.split()[0]}",
        f"Executable: {os.path.abspath(sys.executable) if frozen else '(running from source)'}",
        f"exiftool (full XMP/IPTC copy): {exe or 'NOT FOUND — EXIF + ICC only'}",
    ])


HANDLERS = {
    "photo_info": tool_photo_info,
    "restore_metadata": tool_restore_metadata,
    "process_folders": tool_process_folders,
    "supported_formats": tool_supported_formats,
    "app_info": tool_app_info,
}


def call_tool(name, args):
    fn = HANDLERS.get(name)
    if fn is None:
        return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                "isError": True}
    try:
        ok, text = fn(args or {})
    except Exception as e:
        return {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}],
                "isError": True}
    return {"content": [{"type": "text", "text": text}], "isError": not ok}


# ----------------------------------------------------------------------
# Цикл JSON-RPC 2.0 (stdio)

INSTRUCTIONS = (
    "OriginEcho restores shooting history (EXIF/XMP/IPTC/ICC) that AI photo "
    "editors strip away. Typical flow: photo_info on the original, then "
    "restore_metadata(original, edited) or process_folders(orig_dir, edited_dir)."
)


def _send(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _reply(mid, result):
    _send({"jsonrpc": "2.0", "id": mid, "result": result})


def _fail(mid, code, message):
    _send({"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}})


def handle(msg):
    mid = msg.get("id")
    method = msg.get("method", "")
    params = msg.get("params") or {}

    if mid is None:  # уведомление (notifications/initialized и подобные)
        return

    if method == "initialize":
        _reply(mid, {
            "protocolVersion": params.get("protocolVersion") or PROTOCOL_FALLBACK,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "title": "OriginEcho",
                           "version": __version__},
            "instructions": INSTRUCTIONS,
        })
    elif method == "ping":
        _reply(mid, {})
    elif method == "tools/list":
        _reply(mid, {"tools": TOOLS})
    elif method == "tools/call":
        _reply(mid, call_tool(params.get("name", ""), params.get("arguments")))
    elif method in ("resources/list", "resources/templates/list"):
        _reply(mid, {"resources": []} if method == "resources/list" else {"resourceTemplates": []})
    elif method == "prompts/list":
        _reply(mid, {"prompts": []})
    else:
        _fail(mid, -32601, f"Method not found: {method}")


def main():
    sys.stderr.write(f"OriginEcho MCP server v{__version__} (stdio)\n")
    sys.stderr.flush()
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except Exception:
                _fail(None, -32700, "Parse error")
                continue
            try:
                handle(msg)
            except Exception as e:  # сервер не должен падать из-за одного запроса
                _fail(msg.get("id"), -32603, f"Internal error: {e}")
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
