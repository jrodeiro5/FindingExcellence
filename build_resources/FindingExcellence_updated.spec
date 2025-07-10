# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

a = Analysis(
    ['..\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['openpyxl.cell._writer', 'xlrd', 'pandas'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add icon for the executable - try multiple icon options
icon_path = None
icon_candidates = [
    'icons/FindingExcellence_new_logo.ico',
    'icons/app_icon.ico',
    '../resources/FindingExcellence_new_logo_1.ico'
]

for candidate in icon_candidates:
    if os.path.exists(candidate):
        icon_path = candidate
        break

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FindingExcellence',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path
)
