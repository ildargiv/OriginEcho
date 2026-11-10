# Contributing

Bug reports, ideas and pull requests are welcome.

## Reporting a problem

Open an [issue](https://github.com/ildargiv/OriginEcho/issues) with the program version, the Windows version, the file formats involved (original and edited) and what was lost or copied wrongly. A pair of sample files helps most; remove GPS data first if the place is private. Security problems go through [SECURITY.md](SECURITY.md).

## Running from source

Python 3.11+ on Windows.

```
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File tools\fetch_exiftool.ps1
python tools\gui.py
```

The second line downloads the pinned ExifTool build into `tools\exiftool` (it is not stored in the repository) and checks every file against `tools\exiftool.sha256`. Without ExifTool the program still copies EXIF and ICC.

## Pull requests

- One change per pull request; say which formats you tested.
- Every pull request is built on GitHub: the exe and the installer are compiled and the exe is started as a smoke test.
- Interface strings live in `tools/i18n.py`; a new string needs at least English and Russian.
- To move to a newer ExifTool: change the version in `tools/fetch_exiftool.ps1` and regenerate `tools/exiftool.sha256` from the official download.

Contributions are accepted under the [MIT licence](LICENSE) of the project.
