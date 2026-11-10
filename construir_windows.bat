@echo off
REM Construye la aplicacion para Windows. Ejecutar desde la carpeta del proyecto.
REM Requiere Python 3 de 64 bits instalado (con "Add python.exe to PATH").

python -m venv venv
if errorlevel 1 goto error
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install PyQt5 pyinstaller
if errorlevel 1 goto error

pyinstaller --noconfirm --clean morse_gui_windows.spec
if errorlevel 1 goto error

echo.
echo Listo: dist\morse_gui\morse_gui.exe
pause
exit /b 0

:error
echo.
echo Ha ocurrido un error. Revisa los mensajes anteriores.
pause
exit /b 1
