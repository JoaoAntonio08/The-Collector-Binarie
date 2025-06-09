# -*- mode: python ; coding: utf-8 -*-

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

main_script = 'main_app_fixed.py'
app_name = 'The Collector Binarie'
# Ícone .ico geralmente é ignorado no Linux
# icon_path = os.path.join('resources', 'logo.ico')

# Recursos incluídos
datas = [
    (os.path.join('resources', 'logo.png'), 'resources'),
    ('ui', 'ui')
]

a = Analysis(
    [main_script],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True  # Altere para False se não quiser terminal junto
)

