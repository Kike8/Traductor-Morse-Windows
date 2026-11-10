# -*- mode: python ; coding: utf-8 -*-
# Especificación de PyInstaller para WINDOWS (genera la carpeta dist\morse_gui con morse_gui.exe)
# Uso:  pyinstaller --noconfirm --clean morse_gui_windows.spec


a = Analysis(
    ['morse_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('morse.png', '.')],   # icono de la ventana
    hiddenimports=['PyQt5.QtMultimedia', 'morse_decoder', 'morse_receptor'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='morse_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,        # sin ventana negra; pon True temporalmente para ver errores al arrancar
    disable_windowed_traceback=False,
    icon='morse.ico',     # icono del .exe
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='morse_gui',
)
