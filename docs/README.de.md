# OriginEcho

**Aufnahmegeschichte wiederherstellen, die nach der KI-Bearbeitung verloren ging.**

Wenn Sie ein Foto durch einen KI-Generator oder -Editor schicken, kommt die
Ausgabedatei meist **nackt** heraus: Kameramarke und -modell, Datum und Uhrzeit
der Aufnahme, GPS-Koordinaten, ISO, Belichtung und Objektivdaten sind alle
weg. Das Bild sieht gleich aus, aber seine Geschichte ist verschwunden.

**OriginEcho** gibt diese Geschichte zurück. Es überträgt die vollständigen
Metadaten des Originalfotos auf das KI-bearbeitete Bild — und stellt
optional sogar das Dateiformat wieder her und benennt das Ergebnis um.

---

## Was es tut

| | |
|---|---|
| **EXIF kopieren** | Kamera, Modell, Datum/Zeit, GPS, ISO, Belichtung, Objektiv, Brennweite… |
| **XMP + IPTC kopieren** | Bildbeschreibungen, Künstler, Schlüsselwörter, Bewertung, Verlauf |
| **Farbprofil kopieren** | ICC-Profil, damit die Farben exakt bleiben |
| **Format wiederherstellen** | das KI-Ergebnis wird in das Format des Originals umgewandelt (PNG → JPEG, WEBP → JPEG…) |
| **Ergebnis umbenennen** | `Originalname Bearbeitungsname.ext` |
| **Dateidaten übernehmen** | Erstellungs- und Änderungsdatum wie beim Original |

## Warum

KI-Werkzeuge bauen die Datei neu auf und kennen die Metadaten des Originals
nicht. OriginEcho liest sie aus dem unberührten Original und überträgt sie auf
die bearbeitete Kopie, damit das fertige Bild seine Herkunft behält.

## Schnellstart

1. Doppelklick auf **`OriginEcho.bat`** (Windows) — das Programmfenster öffnet sich.
2. Wählen Sie unter **ORIGINAL** das unberührte Foto (oder einen Ordner).
3. Wählen Sie unter **BEARBEITETE FOTOS** das KI-Ergebnis (Datei, mehrere
   Dateien oder Ordner). Sie können Dateien auch **per Drag & Drop** direkt in
   die Felder ziehen.
4. Klicken Sie auf **ÜBERTRAGUNG STARTEN**.

Das Ergebnis erscheint neben der bearbeiteten Datei, benannt als
`<Originalname> <Name der Bearbeitung>.<Originalendung>`.

### Optionen

- **Format wie Original** — auf das Originalformat umwandeln.
- **Name: Original + Kopie** — in „Original + Leerzeichen + Kopie“ umbenennen.
- **Alte Datei löschen** — die Datei vor dem Umbenennen danach entfernen.
- **Dateidaten kopieren** — Erstellungs-/Änderungszeit übernehmen.

## Kommandozeile

```bash
python tools/copy_photo_metadata.py original.jpg bearbeitet.jpg [mehr.jpg ...]
python tools/copy_photo_metadata.py --folder ORIGINALE_BEARBEITET
```

Schalter: `--no-icc`, `--no-dates`, `--no-convert`, `--no-rename`, `--keep-old`.

## Unterstützte Sprachen

Die Oberfläche ist in **11 Sprachen** verfügbar — wählen Sie oben rechts im
Fenster; die Auswahl wird gespeichert:

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## Unterstützte Dateiformate

Ein-/Ausgabe: **JPEG, PNG, WEBP, TIFF**. HEIC wird unterstützt, wenn
`pillow-heif` installiert ist.

## Hinweise & Qualität

- Bei **JPEG → JPEG** bearbeitet OriginEcho die Datei auf Byte-Ebene, sodass die
  Bilddaten **verlustfrei** erhalten bleiben — ohne Neukomprimierung.
- Die Umwandlung zwischen Formaten (z. B. PNG → JPEG) kodiert das Bild
  zwangsläufig neu.
- Transparente PNG/WEBP werden bei der Umwandlung nach JPEG auf Weiß gelegt.
- PNG und WEBP unterstützen einige EXIF-Felder nur eingeschränkt (eine
  Beschränkung der Formate). Für die vollständigen Daten ist JPEG besser.
- Die vollständige Übertragung (XMP/IPTC) übernimmt **exiftool** (in
  `tools/exiftool`); ohne sie beschränkt sich das Programm auf EXIF + ICC.

## Voraussetzungen

- Python 3.11+
- Pillow (wird bei Bedarf automatisch nachinstalliert)
- `tkinterdnd2` — Drag & Drop (optional)
- exiftool — vollständiges XMP/IPTC (optional, mitgeliefert)

## Danksagungen

- **exiftool** von Phil Harvey — der Goldstandard für Bildmetadaten.
- **Pillow** — Bilddekodierung/-kodierung.
- **tkinterdnd2** — Drag-&-Drop-Unterstützung für Tkinter.

## Lizenz

MIT — frei verwendbar und änderbar.

---

<p align="center"><sub>English: <a href="../README.md">EN</a> ·
<a href="README.ru.md">RU</a> · <a href="README.es.md">ES</a> ·
<a href="README.fr.md">FR</a> · <a href="README.it.md">IT</a> ·
<a href="README.tr.md">TR</a> · <a href="README.hi.md">HI</a> ·
<a href="README.id.md">ID</a> · <a href="README.ko.md">KO</a> ·
<a href="README.zh.md">ZH</a></sub></p>
