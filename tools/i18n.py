# -*- coding: utf-8 -*-
"""OriginEcho — мультиязычный словарь интерфейса.

OriginEcho возвращает обработанной ИИ фотографии данные оригинала:
историю съёмки (EXIF) и формат файла.
"""

LANGS = {
    "ru": "Русский",
    "en": "English",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
    "tr": "Türkçe",
    "hi": "हिन्दी",
    "id": "Bahasa Indonesia",
    "ko": "한국어",
    "zh": "中文",
}

# Шрифт по умолчанию; для CJK/деванагари — свои
FONT = {
    "zh": "Microsoft YaHei UI",
    "ko": "Malgun Gothic",
    "hi": "Nirmala UI",
    "tr": "Segoe UI",
    "en": "Segoe UI", "ru": "Segoe UI", "de": "Segoe UI", "es": "Segoe UI",
    "fr": "Segoe UI", "it": "Segoe UI", "id": "Segoe UI",
}
DEFAULT_LANG = "ru"

# базовый набор ключей (английский как fallback)
EN = {
    "app_name": "OriginEcho",
    "app_title": "OriginEcho — Restore Shooting History",
    "tagline": "Transfers the original photo's data (camera, date, GPS, ISO) "
              "and file format to the AI-edited photo.",
    "c1_title": "ORIGINAL", "c1_sub": "Source of data and file type",
    "c2_title": "EDITED PHOTOS", "c2_sub": "Destination — files or folder",
    "c3_title": "RUN", "c3_sub": "Processing result",
    "btn_file": "File", "btn_folder": "Folder", "btn_run": "RUN TRANSFER",
    "opt_format": "Format as original", "opt_rename": "Name: original + copy",
    "opt_delete": "Delete old file", "opt_dates": "Copy file dates",
    "hint": "Drag files into the fields. Full transfer: {meta}.",
    "meta_on": "XMP/IPTC on", "meta_off": "exiftool not found",
    "lang_label": "Language",
    "summary_none": "EXIF present", "summary_fail": "Could not read file",
    "log_start": "Working…",
    "warn_nothing": "Select the original and the edited photos.",
    "warn_title": "Nothing selected",
    "err_kinds": "Source and destination must both be files or both folders.",
    "err_prog": "Program error",
    "ok_fmt": "written",
}

RU = {
    "app_title": "OriginEcho — Восстановление истории съёмки",
    "tagline": "Переносит все данные исходной фотографии (камера, дата, GPS, "
              "ISO) и её формат на файл, обработанный ИИ.",
    "c1_title": "ОРИГИНАЛ", "c1_sub": "Откуда берём данные и тип файла",
    "c2_title": "ОБРАБОТАННЫЕ ФОТО", "c2_sub": "Куда записываем — файлы или папка",
    "c3_title": "ЗАПУСК", "c3_sub": "Результат обработки",
    "btn_file": "Файл", "btn_folder": "Папка", "btn_run": "ВЫПОЛНИТЬ ПЕРЕНОС",
    "opt_format": "Формат как у оригинала", "opt_rename": "Имя: оригинал + копия",
    "opt_delete": "Удалить старый файл", "opt_dates": "Скопировать даты файлов",
    "hint": "Перетащите файлы в поля. Полный перенос: {meta}.",
    "meta_on": "XMP/IPTC включён", "meta_off": "exiftool не найден",
    "lang_label": "Язык",
    "summary_none": "EXIF есть", "summary_fail": "Не удалось прочитать файл",
    "log_start": "Выполняю…",
    "warn_nothing": "Выберите оригинал и обработанные фото.",
    "warn_title": "Не выбрано",
    "err_kinds": "Источник и цель должны быть обоими файлами или обоими папками.",
    "err_prog": "Ошибка программы",
    "ok_fmt": "записан",
}


DE = {
    "app_title": "OriginEcho — Aufnahmegeschichte wiederherstellen",
    "tagline": "Überträgt die Daten des Originalfotos (Kamera, Datum, GPS, ISO) "
              "und dessen Format auf das KI-bearbeitete Foto.",
    "c1_title": "ORIGINAL", "c1_sub": "Quelle der Daten und des Dateityps",
    "c2_title": "BEARBEITETE FOTOS", "c2_sub": "Ziel — Dateien oder Ordner",
    "c3_title": "AUSFÜHREN", "c3_sub": "Ergebnis der Verarbeitung",
    "btn_file": "Datei", "btn_folder": "Ordner", "btn_run": "ÜBERTRAGUNG STARTEN",
    "opt_format": "Format wie Original", "opt_rename": "Name: Original + Kopie",
    "opt_delete": "Alte Datei löschen", "opt_dates": "Dateidaten kopieren",
    "hint": "Dateien in die Felder ziehen. Vollständige Übertragung: {meta}.",
    "meta_on": "XMP/IPTC aktiv", "meta_off": "exiftool nicht gefunden",
    "lang_label": "Sprache",
    "summary_none": "EXIF vorhanden", "summary_fail": "Datei nicht lesbar",
    "log_start": "Wird ausgeführt…",
    "warn_nothing": "Original und bearbeitete Fotos auswählen.",
    "warn_title": "Nichts ausgewählt",
    "err_kinds": "Quelle und Ziel müssen beide Dateien oder beide Ordner sein.",
    "err_prog": "Programmfehler",
    "ok_fmt": "geschrieben",
}

ES = {
    "app_title": "OriginEcho — Restaurar historial de captura",
    "tagline": "Transfiere los datos de la foto original (cámara, fecha, GPS, "
              "ISO) y su formato a la foto editada por IA.",
    "c1_title": "ORIGINAL", "c1_sub": "Origen de los datos y tipo de archivo",
    "c2_title": "FOTOS EDITADAS", "c2_sub": "Destino — archivos o carpeta",
    "c3_title": "EJECUTAR", "c3_sub": "Resultado del proceso",
    "btn_file": "Archivo", "btn_folder": "Carpeta", "btn_run": "REALIZAR TRANSFERENCIA",
    "opt_format": "Formato como el original", "opt_rename": "Nombre: original + copia",
    "opt_delete": "Eliminar archivo antiguo", "opt_dates": "Copiar fechas",
    "hint": "Arrastra los archivos a los campos. Transferencia completa: {meta}.",
    "meta_on": "XMP/IPTC activado", "meta_off": "exiftool no encontrado",
    "lang_label": "Idioma",
    "summary_none": "EXIF presente", "summary_fail": "No se pudo leer el archivo",
    "log_start": "Procesando…",
    "warn_nothing": "Selecciona el original y las fotos editadas.",
    "warn_title": "Nada seleccionado",
    "err_kinds": "Origen y destino deben ser ambos archivos o ambas carpetas.",
    "err_prog": "Error del programa",
    "ok_fmt": "escrito",
}

FR = {
    "app_title": "OriginEcho — Restaurer l’historique de prise de vue",
    "tagline": "Transfère les données de la photo d’origine (appareil, date, "
              "GPS, ISO) et son format vers la photo retouchée par l’IA.",
    "c1_title": "ORIGINALE", "c1_sub": "Source des données et du format",
    "c2_title": "PHOTOS RETOUCHÉES", "c2_sub": "Destination — fichiers ou dossier",
    "c3_title": "EXÉCUTION", "c3_sub": "Résultat du traitement",
    "btn_file": "Fichier", "btn_folder": "Dossier", "btn_run": "LANCER LE TRANSFERT",
    "opt_format": "Format comme l’original", "opt_rename": "Nom : original + copie",
    "opt_delete": "Supprimer l’ancien fichier", "opt_dates": "Copier les dates",
    "hint": "Glissez les fichiers dans les champs. Transfert complet : {meta}.",
    "meta_on": "XMP/IPTC activé", "meta_off": "exiftool introuvable",
    "lang_label": "Langue",
    "summary_none": "EXIF présent", "summary_fail": "Lecture du fichier impossible",
    "log_start": "Traitement…",
    "warn_nothing": "Sélectionnez l’original et les photos retouchées.",
    "warn_title": "Aucune sélection",
    "err_kinds": "La source et la cible doivent être des fichiers ou des dossiers.",
    "err_prog": "Erreur du programme",
    "ok_fmt": "écrit",
}

IT = {
    "app_title": "OriginEcho — Ripristina la cronologia dello scatto",
    "tagline": "Trasferisce i dati della foto originale (telecamera, data, GPS, "
              "ISO) e il suo formato alla foto modificata dall’IA.",
    "c1_title": "ORIGINALE", "c1_sub": "Origine dei dati e tipo di file",
    "c2_title": "FOTO MODIFICATE", "c2_sub": "Destinazione — file o cartella",
    "c3_title": "ESEGUI", "c3_sub": "Risultato dell’elaborazione",
    "btn_file": "File", "btn_folder": "Cartella", "btn_run": "AVVIA TRASFERIMENTO",
    "opt_format": "Formato come l’originale", "opt_rename": "Nome: originale + copia",
    "opt_delete": "Elimina il vecchio file", "opt_dates": "Copia le date",
    "hint": "Trascina i file nei campi. Trasferimento completo: {meta}.",
    "meta_on": "XMP/IPTC attivo", "meta_off": "exiftool non trovato",
    "lang_label": "Lingua",
    "summary_none": "EXIF presente", "summary_fail": "Impossibile leggere il file",
    "log_start": "Elaborazione…",
    "warn_nothing": "Seleziona l’originale e le foto modificate.",
    "warn_title": "Nessuna selezione",
    "err_kinds": "Origine e destinazione devono essere entrambe file o cartelle.",
    "err_prog": "Errore del programma",
    "ok_fmt": "scritto",
}


TR = {
    "app_title": "OriginEcho — Çekim Geçmişini Geri Yükle",
    "tagline": "Orijinal fotoğrafın verilerini (kamera, tarih, GPS, ISO) ve "
              "biçimini yapay zekâ ile düzenlenmiş fotoğrafa aktarır.",
    "c1_title": "ORİJİNAL", "c1_sub": "Veri ve dosya türünün kaynağı",
    "c2_title": "DÜZENLENMİŞ FOTOĞRAFLAR", "c2_sub": "Hedef — dosyalar veya klasör",
    "c3_title": "ÇALIŞTIR", "c3_sub": "İşleme sonucu",
    "btn_file": "Dosya", "btn_folder": "Klasör", "btn_run": "AKTARIMI BAŞLAT",
    "opt_format": "Orijinal biçimde", "opt_rename": "Ad: orijinal + kopya",
    "opt_delete": "Eski dosyayı sil", "opt_dates": "Dosya tarihlerini kopyala",
    "hint": "Dosyaları alanlara sürükleyin. Tam aktarım: {meta}.",
    "meta_on": "XMP/IPTC etkin", "meta_off": "exiftool bulunamadı",
    "lang_label": "Dil",
    "summary_none": "EXIF mevcut", "summary_fail": "Dosya okunamadı",
    "log_start": "Çalışıyor…",
    "warn_nothing": "Orijinali ve düzenlenmiş fotoğrafları seçin.",
    "warn_title": "Seçim yapılmadı",
    "err_kinds": "Kaynak ve hedef ikisi de dosya veya ikisi de klasör olmalı.",
    "err_prog": "Program hatası",
    "ok_fmt": "yazıldı",
}

HI = {
    "app_title": "OriginEcho — शूटिंग इतिहास बहाल करें",
    "tagline": "मूल फ़ोटो के सारे डेटा (कैमरा, तारीख, GPS, ISO) और उसका "
              "फ़ॉर्मेट AI-संपादित फ़ोटो पर कॉपी करता है।",
    "c1_title": "मूल फ़ोटो", "c1_sub": "डेटा और फ़ाइल प्रकार का स्रोत",
    "c2_title": "संपादित फ़ोटो", "c2_sub": "गंतव्य — फ़ाइलें या फ़ोल्डर",
    "c3_title": "चलाएँ", "c3_sub": "प्रसंस्करण का परिणाम",
    "btn_file": "फ़ाइल", "btn_folder": "फ़ोल्डर", "btn_run": "ट्रांसफ़र शुरू करें",
    "opt_format": "मूल जैसा फ़ॉर्मेट", "opt_rename": "नाम: मूल + कॉपी",
    "opt_delete": "पुरानी फ़ाइल हटाएँ", "opt_dates": "फ़ाइल तिथियाँ कॉपी करें",
    "hint": "फ़ाइलें खानों में खींचें। पूर्ण ट्रांसफ़र: {meta}.",
    "meta_on": "XMP/IPTC चालू", "meta_off": "exiftool नहीं मिला",
    "lang_label": "भाषा",
    "summary_none": "EXIF मौजूद", "summary_fail": "फ़ाइल नहीं पढ़ी जा सकी",
    "log_start": "चल रहा है…",
    "warn_nothing": "मूल और संपादित फ़ोटो चुनें।",
    "warn_title": "कुछ चुना नहीं",
    "err_kinds": "स्रोत और गंतव्य दोनों फ़ाइल या दोनों फ़ोल्डर होने चाहिए।",
    "err_prog": "प्रोग्राम त्रुटि",
    "ok_fmt": "लिखा गया",
}

ID = {
    "app_title": "OriginEcho — Pulihkan Riwayat Pemotretan",
    "tagline": "Menyalin semua data foto asli (kamera, tanggal, GPS, ISO) dan "
              "formatnya ke foto yang telah diedit AI.",
    "c1_title": "ASLI", "c1_sub": "Sumber data dan jenis berkas",
    "c2_title": "FOTO HASIL EDIT", "c2_sub": "Tujuan — berkas atau folder",
    "c3_title": "JALANKAN", "c3_sub": "Hasil pemrosesan",
    "btn_file": "Berkas", "btn_folder": "Folder", "btn_run": "MULAI SALIN",
    "opt_format": "Format seperti asli", "opt_rename": "Nama: asli + salinan",
    "opt_delete": "Hapus berkas lama", "opt_dates": "Salin tanggal berkas",
    "hint": "Seret berkas ke kolom. Salinan lengkap: {meta}.",
    "meta_on": "XMP/IPTC aktif", "meta_off": "exiftool tidak ditemukan",
    "lang_label": "Bahasa",
    "summary_none": "EXIF ada", "summary_fail": "Gagal membaca berkas",
    "log_start": "Memproses…",
    "warn_nothing": "Pilih foto asli dan foto hasil edit.",
    "warn_title": "Belum ada pilihan",
    "err_kinds": "Sumber dan tujuan harus keduanya berkas atau keduanya folder.",
    "err_prog": "Kesalahan program",
    "ok_fmt": "tertulis",
}


KO = {
    "app_title": "OriginEcho — 촬영 기록 복원",
    "tagline": "원본 사진의 데이터(카메라, 날짜, GPS, ISO)와 파일 형식을 "
              "AI로 편집한 사진에 그대로 옮깁니다.",
    "c1_title": "원본", "c1_sub": "데이터와 파일 형식의 출처",
    "c2_title": "편집된 사진", "c2_sub": "대상 — 파일 또는 폴더",
    "c3_title": "실행", "c3_sub": "처리 결과",
    "btn_file": "파일", "btn_folder": "폴더", "btn_run": "옮기기 실행",
    "opt_format": "원본과 같은 형식", "opt_rename": "이름: 원본 + 사본",
    "opt_delete": "기존 파일 삭제", "opt_dates": "파일 날짜 복사",
    "hint": "파일을 칸으로 끌어다 놓으세요. 전체 복사: {meta}.",
    "meta_on": "XMP/IPTC 사용", "meta_off": "exiftool 없음",
    "lang_label": "언어",
    "summary_none": "EXIF 있음", "summary_fail": "파일을 읽을 수 없음",
    "log_start": "처리 중…",
    "warn_nothing": "원본과 편집된 사진을 선택하세요.",
    "warn_title": "선택 안 됨",
    "err_kinds": "원본과 대상이 모두 파일이거나 모두 폴더여야 합니다.",
    "err_prog": "프로그램 오류",
    "ok_fmt": "기록됨",
}

ZH = {
    "app_title": "OriginEcho — 还原拍摄信息",
    "tagline": "将原始照片的全部数据（相机、日期、GPS、ISO）及其格式，"
              "复制到经 AI 处理后的照片上。",
    "c1_title": "原图", "c1_sub": "数据与文件格式的来源",
    "c2_title": "已处理照片", "c2_sub": "目标 — 文件或文件夹",
    "c3_title": "执行", "c3_sub": "处理结果",
    "btn_file": "文件", "btn_folder": "文件夹", "btn_run": "开始复制",
    "opt_format": "与原图相同格式", "opt_rename": "命名：原图 + 副本",
    "opt_delete": "删除旧文件", "opt_dates": "复制文件日期",
    "hint": "将文件拖入字段。完整复制：{meta}。",
    "meta_on": "XMP/IPTC 已启用", "meta_off": "未找到 exiftool",
    "lang_label": "语言",
    "summary_none": "含 EXIF", "summary_fail": "无法读取文件",
    "log_start": "处理中…",
    "warn_nothing": "请选择原图和已处理的照片。",
    "warn_title": "未选择",
    "err_kinds": "源和目标必须同为文件或同为文件夹。",
    "err_prog": "程序错误",
    "ok_fmt": "已写入",
}

_T = {"ru": RU, "de": DE, "es": ES, "fr": FR, "it": IT,
      "tr": TR, "hi": HI, "id": ID, "ko": KO, "zh": ZH}

# ---- сообщения журнала/ошибок ----
M = {
 "en": dict(e_src="Source not found", e_dst="Target file not found",
   e_same="Source and target are the same", ok_exif="metadata written",
   ok_unsup="EXIF not supported by this format", ok_xmp="+ XMP/IPTC",
   del_old="old file deleted", keep_old="old file NOT deleted (in use?)",
   fmt="format {f}", no_pair="original not found"),
 "ru": dict(e_src="Источник не найден", e_dst="Целевой файл не найден",
   e_same="Источник и цель совпадают", ok_exif="данные записаны",
   ok_unsup="EXIF не поддерживается форматом", ok_xmp="+ XMP/IPTC",
   del_old="старый удалён", keep_old="старый НЕ удалён (занят?)",
   fmt="формат {f}", no_pair="оригинал не найден"),
 "de": dict(e_src="Quelle nicht gefunden", e_dst="Zieldatei nicht gefunden",
   e_same="Quelle und Ziel identisch", ok_exif="Metadaten geschrieben",
   ok_unsup="EXIF in diesem Format nicht unterstützt", ok_xmp="+ XMP/IPTC",
   del_old="alte Datei gelöscht", keep_old="alte Datei NICHT gelöscht (belegt?)",
   fmt="Format {f}", no_pair="Original nicht gefunden"),
 "es": dict(e_src="Origen no encontrado", e_dst="Archivo destino no encontrado",
   e_same="Origen y destino son iguales", ok_exif="datos escritos",
   ok_unsup="EXIF no admitido en este formato", ok_xmp="+ XMP/IPTC",
   del_old="archivo antiguo eliminado", keep_old="archivo antiguo NO eliminado (¿ocupado?)",
   fmt="formato {f}", no_pair="original no encontrado"),
 "fr": dict(e_src="Source introuvable", e_dst="Fichier cible introuvable",
   e_same="Source et cible identiques", ok_exif="données écrites",
   ok_unsup="EXIF non pris en charge dans ce format", ok_xmp="+ XMP/IPTC",
   del_old="ancien fichier supprimé", keep_old="ancien fichier NON supprimé (occupé ?)",
   fmt="format {f}", no_pair="original introuvable"),
 "it": dict(e_src="Origine non trovata", e_dst="File di destinazione non trovato",
   e_same="Origine e destinazione uguali", ok_exif="dati scritti",
   ok_unsup="EXIF non supportato in questo formato", ok_xmp="+ XMP/IPTC",
   del_old="vecchio file eliminato", keep_old="vecchio file NON eliminato (occupato?)",
   fmt="formato {f}", no_pair="originale non trovato"),
 "tr": dict(e_src="Kaynak bulunamadı", e_dst="Hedef dosya bulunamadı",
   e_same="Kaynak ve hedef aynı", ok_exif="veri yazıldı",
   ok_unsup="EXIF bu formatta desteklenmiyor", ok_xmp="+ XMP/IPTC",
   del_old="eski dosya silindi", keep_old="eski dosya SİLİNMEDİ (meşgul?)",
   fmt="biçim {f}", no_pair="orijinal bulunamadı"),
 "hi": dict(e_src="स्रोत नहीं मिला", e_dst="लक्ष्य फ़ाइल नहीं मिली",
   e_same="स्रोत और लक्ष्य समान हैं", ok_exif="डेटा लिखा गया",
   ok_unsup="इस प्रारूप में EXIF समर्थित नहीं", ok_xmp="+ XMP/IPTC",
   del_old="पुरानी फ़ाइल हटाई गई", keep_old="पुरानी फ़ाइल नहीं हटी (व्यस्त?)",
   fmt="प्रारूप {f}", no_pair="मूल नहीं मिला"),
 "id": dict(e_src="Sumber tidak ditemukan", e_dst="Berkas tujuan tidak ditemukan",
   e_same="Sumber dan tujuan sama", ok_exif="data ditulis",
   ok_unsup="EXIF tidak didukung pada format ini", ok_xmp="+ XMP/IPTC",
   del_old="berkas lama dihapus", keep_old="berkas lama TIDAK dihapus (sedang dipakai?)",
   fmt="format {f}", no_pair="asli tidak ditemukan"),
 "ko": dict(e_src="원본을 찾을 수 없음", e_dst="대상 파일을 찾을 수 없음",
   e_same="원본과 대상이 같음", ok_exif="데이터 기록됨",
   ok_unsup="이 형식은 EXIF 미지원", ok_xmp="+ XMP/IPTC",
   del_old="기존 파일 삭제됨", keep_old="기존 파일 삭제 안 됨(사용 중?)",
   fmt="형식 {f}", no_pair="원본을 찾을 수 없음"),
 "zh": dict(e_src="未找到源文件", e_dst="未找到目标文件",
   e_same="源与目标相同", ok_exif="数据已写入",
   ok_unsup="此格式不支持 EXIF", ok_xmp="+ XMP/IPTC",
   del_old="已删除旧文件", keep_old="未删除旧文件（被占用？）",
   fmt="格式 {f}", no_pair="未找到原图"),
}
for _c, _d in M.items():
    _T.setdefault(_c, {}).update(_d)


def tm(key, lang):
    """Сообщение журнала с fallback на английский."""
    return _T.get(lang, {}).get(key) or _T["en"].get(key, key)


def t(key, lang):
    lang = lang or DEFAULT_LANG
    if lang == "en":
        return EN.get(key, key)
    return _T.get(lang, {}).get(key, EN.get(key, key))


def font_family(lang):
    return FONT.get(lang, "Segoe UI")
