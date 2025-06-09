# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Função auxiliar para obter caminho de recursos (compatível com PyInstaller)
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Caminho para o script principal
main_script = 'main_app_fixed.py'

# Nome do aplicativo
app_name = 'The Collector Binarie'

# Ícone do aplicativo
icon_path = os.path.join('resources', 'logo.ico')

# Arquivos e diretórios a serem incluídos (dados)
# O formato é uma lista de tuplas: ('caminho/origem', 'caminho/destino/no/bundle')
datas = [
    (os.path.join('resources', 'logo.png'), 'resources'), # Inclui o logo
    ('ui', 'ui'), # Inclui todo o diretório ui
    ('user_settings.ini', '.'), # Inclui o arquivo de configurações do usuário
    ('main_app.log', '.') # Inclui o arquivo de log principal
]

# Opções de análise
block_cipher = None

# Configuração do executável
a = Analysis(
    [main_script],
    pathex=['.'], # Adiciona o diretório atual ao path
    binaries=[],
    datas=datas,
    hiddenimports=[], # Adicionar aqui se PyInstaller falhar em encontrar algo
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

# Configuração do executável final
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # False para aplicações GUI (não mostra console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path, # Define o ícone
)

# Se for macOS, configurar o bundle
# app = BUNDLE(...) # Descomentar e configurar para macOS se necessário

