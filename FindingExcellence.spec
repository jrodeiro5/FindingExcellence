# -*- mode: python ; coding: utf-8 -*-
# FindingExcellence.spec
# PyInstaller build specification

import sys
from pathlib import Path

block_cipher = None

# Project root (where this .spec lives)
ROOT = Path(SPECPATH)

a = Analysis(
    [str(ROOT / 'main.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # Include the resources folder (icons, etc.) inside the exe bundle
        (str(ROOT / 'resources'), 'resources'),
    ],
    hiddenimports=[
        'ttkbootstrap',
        'ttkbootstrap.themes',
        'ttkbootstrap.style',
        'PIL',
        'PIL.Image',
        'openpyxl',
        'xlrd',
        'tkcalendar',
        'babel.numbers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FindingExcellence',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,           # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Icon embedded directly into the .exe file
    icon=str(ROOT / 'resources' / 'FindingExcellence_new_logo_1.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FindingExcellence',
)
