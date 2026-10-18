# OriginEcho

**Restore shooting history lost after AI photo editing.**

When you run a photograph through an AI generator or editor, the exported file
usually comes out **naked**: the camera make and model, the date and time you
pressed the shutter, GPS coordinates, ISO, exposure and lens information are all
stripped away. The picture looks the same, but its story is gone.

**OriginEcho** gives that story back. It copies the original photo's complete
metadata onto the AI-edited image — and, optionally, restores the original file
format and names the result for you.

It also runs as an **MCP server** — AI assistants like Claude Desktop, OpenCode
or Cursor can restore the metadata for you in plain language, see
[AI agents (MCP)](#ai-agents-mcp).

---

## ⬇️ Download

**[Latest release — OriginEcho](https://github.com/ildargiv/OriginEcho/releases/latest)**

| File | For whom |
|---|---|
| `OriginEcho-Setup-*.exe` | Windows installer — recommended, install and run |
| `OriginEcho.exe` | portable version — just download and double-click |

Windows 10/11 (64-bit). **Python is not required** — everything is included.

---

## What it does

| | |
|---|---|
| **Copies EXIF** | camera, model, date/time, GPS, ISO, exposure, lens, focal length… |
| **Copies XMP + IPTC** | captions, author/artist, keywords, ratings, edit history |
| **Copies the color profile** | ICC profile, so colors stay exactly as intended |
| **Restores the format** | the AI result is converted back to the original's format (PNG → JPEG, WEBP → JPEG…) |
| **Renames the result** | `original-name edited-name.ext` — exactly as you asked |
| **Restores file dates** | "created" and "modified" timestamps match the original |

## Why

AI tools rewrite the file from scratch and do not know your original metadata.
OriginEcho reads it from the untouched original and grafts it onto the edited
copy, so the finished photo keeps its provenance.

## Quick start

1. Double-click **`OriginEcho.bat`** (Windows) — the program window opens.
2. In **ORIGINAL**, choose the untouched photo (or a folder of originals).
3. In **EDITED PHOTOS**, choose the AI output (a file, several files, or a folder).
   You can also **drag and drop** files straight into the fields.
4. Press **RUN TRANSFER**.

The result appears next to the edited file, renamed
`<original name> <edited name>.<original extension>`.

### Options

- **Format as original** — convert the edited file to the original's format.
- **Name: original + copy** — rename the result to `original + space + copy`.
- **Delete old file** — remove the pre-rename copy after a successful transfer.
- **Copy file dates** — apply the original's created/modified timestamps.

## Command line

```bash
python tools/copy_photo_metadata.py original.jpg edited.jpg [more.jpg ...]
python tools/copy_photo_metadata.py --folder ORIGINALS_DIR EDITED_DIR
```

Flags: `--no-icc`, `--no-dates`, `--no-convert`, `--no-rename`, `--keep-old`.

## AI agents (MCP)

OriginEcho can run as an **MCP server** (Model Context Protocol), so AI assistants —
Claude Desktop, OpenCode, Cursor and similar — can restore metadata for you in plain
language.

Run the same `OriginEcho.exe` with the `--mcp` flag (stdio transport, local only,
no ports and no network traffic):

```json
{
  "mcpServers": {
    "originecho": {
      "command": "C:\\Program Files\\OriginEcho\\OriginEcho.exe",
      "args": ["--mcp"]
    }
  }
}
```

From source: `"command": "python", "args": ["C:\\path\\to\\tools\\mcp_server.py"]`.

Tools the agent gets:

| Tool | What it does |
|---|---|
| `photo_info` | Read the shooting history of a file (camera, date, ISO, GPS...) |
| `restore_metadata` | Copy EXIF/XMP/IPTC/ICC from the original onto an edited photo |
| `process_folders` | Batch-process two folders |
| `supported_formats` | List supported formats |
| `app_info` | Version and component check |

Example prompt: *"Transfer the metadata from IMG_20261017_142755.jpg to every photo
in the Edited folder."*

## Supported languages

The interface is available in **11 languages** — pick one in the top-right corner
of the window; your choice is remembered:

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## Supported file formats

Input/output: **JPEG, PNG, WEBP, TIFF**. HEIC is supported when `pillow-heif`
is installed.

## Notes & quality

- For **JPEG → JPEG**, OriginEcho edits the file at the byte level, so the image
  data is preserved **losslessly** — no re-compression, no quality loss.
- Converting between formats (e.g. PNG → JPEG) necessarily re-encodes the image.
- Transparent PNG/WEBP are flattened onto a white background when converted to
  JPEG.
- PNG and WEBP have limited support for some EXIF fields (a limitation of those
  formats, not the program). For the full record, prefer a JPEG result.
- Full metadata (XMP/IPTC) is copied with **exiftool** (bundled in
  `tools/exiftool`); without it the program falls back to EXIF + ICC.

## Requirements

- Python 3.11+
- Pillow (installed automatically on first run if missing)
- `tkinterdnd2` — for drag & drop (optional)
- exiftool — for full XMP/IPTC (optional, bundled)

## Credits

- **exiftool** by Phil Harvey — the gold standard for image metadata.
- **Pillow** — image decoding/encoding.
- **tkinterdnd2** — drag & drop support for Tkinter.

## License

MIT — free to use and modify.

---

<p align="center"><sub>Translations: <a href="docs/README.ru.md">RU</a> ·
<a href="docs/README.de.md">DE</a> · <a href="docs/README.es.md">ES</a> ·
<a href="docs/README.fr.md">FR</a> · <a href="docs/README.it.md">IT</a> ·
<a href="docs/README.tr.md">TR</a> · <a href="docs/README.hi.md">HI</a> ·
<a href="docs/README.id.md">ID</a> · <a href="docs/README.ko.md">KO</a> ·
<a href="docs/README.zh.md">ZH</a></sub></p>
