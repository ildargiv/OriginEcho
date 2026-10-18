# -*- mode: python ; coding: utf-8 -*-
"""Сборка OriginEcho.exe (PyInstaller, один файл).

    pyinstaller OriginEcho.spec --noconfirm --clean

exiftool кладётся внутрь exe (tools/exiftool), tkinterdnd2 — вместе с
файлами tkdnd (только Windows-сборки, Linux/macOS отбрасываем).

Консоль включена: stdio-транспорту режима --mcp (MCP-сервер для ИИ-агентов)
нужны настоящие stdin/stdout. В GUI-режиме окно консоли скрывается сразу
по запуска (см. main() в gui.py)."""
from PyInstaller.utils.hooks import collect_data_files

SPECDIR = SPECPATH

datas = [(f"{SPECDIR}/tools/exiftool", "tools/exiftool")]
_tkdnd = collect_data_files("tkinterdnd2")
datas += [(src, dest) for src, dest in _tkdnd
          if not any(s in str(src).lower()
                     for s in ("linux", "macosx", "darwin"))]

a = Analysis(
    [f"{SPECDIR}/tools/gui.py"],
    pathex=[f"{SPECDIR}/tools"],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="OriginEcho",
    debug=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    icon=f"{SPECDIR}/icon.ico",
)
