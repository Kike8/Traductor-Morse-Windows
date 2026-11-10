# Traductor-Morse-Windows 

# Traductor_Morse
App que traduce texto a código morse y viceversa con capacidad de escucha y grabación

MORSE_DECODER.PY el cerebro de la aplicación

__init__: calcula el tamaño del tramo de análisis (5 ms) y el filtro que elimina el zumbido y la componente continua.
Ajustes : set_wpm (velocidad), set_adaptive (modo Auto) y set_sensitivity (nivel mínimo de detección). La propiedad wpm devuelve la velocidad en uso.
reset: deja todo el estado a cero (ruido, grupo en curso, etc.).
feed: punto de entrada. Recibe muestras de audio, las corta en tramos de 5 ms y devuelve el Morse nuevo detectado.
flush: fuerza decodificar lo pendiente, para que no se quede la última letra sin salir al detener la escucha.
_frame_level: calcula el volumen (RMS) de un tramo, tras quitar la componente continua.
_step: decide en cada tramo si hay tono o silencio. Mide primero el ruido de fondo y usa un umbral adaptativo con histéresis y filtro anti-rebotes de 15 ms.
_cambiar_estado y _fin_de_tono: registran la duración de cada bip y de cada pausa. Descartan los clics demasiado cortos y las portadoras demasiado largas.
_comprobar_silencio: cuando la pausa es larga cierra el grupo y decodifica. Después inserta el espacio entre letras (≥ 2 unidades) y la / entre palabras (≥ 5 unidades).
_estimar_unidad: detecta la velocidad automáticamente. Agrupa las duraciones en dos clústeres (cortos y largos) y deduce la unidad de tiempo.
_decodificar_grupo: con esa unidad clasifica cada bip (menos de 2 unidades es ., el resto es -) y coloca los separadores.
_pcm_a_enteros: convierte WAV de 8, 16, 24 o 32 bits, mono o estéreo, a muestras de 16 bits.
decodificar_wav: lee un archivo WAV y lo pasa por el decodificador.

MORSE_RECEPTOR.PY: CAPTURA DE AUDIO Y PANEL (QT)

NivelWidget: la barra de nivel en dB. Es verde con tono y azul sin él, y la línea naranja marca el umbral.
ReceptorMorse: el panel. Define dos señales: morse_decodificado (Morse nuevo en directo) y bloque_decodificado (resultado de un WAV).
_build_ui: crea los botones, el selector de entrada, la velocidad (WPM), la casilla Auto, la sensibilidad, el medidor y el estado.
_llenar_dispositivos: lista las entradas de audio y pone primero la predeterminada.
Aplican los cambios de velocidad, Auto y sensibilidad al decodificador.
alternar / iniciar: piden formato PCM de 16 bits a 8000 Hz, crean el decodificador, abren QAudioInput y arrancan un temporizador de 30 ms que lee el audio.
detener y _liberar_audio: leen lo que queda, hacen flush y liberan el audio y el temporizador.
_on_ready_read: lee los bytes y los convierte en muestras. Mantiene los bytes sobrantes entre lecturas, se queda con el primer canal si es estéreo, llama a feed y emite el texto Morse. Actualiza también el medidor.
_diagnostico: a los ~2 s avisa en rojo si no llega audio o llega solo silencio (permisos).
analizar_wav: abre un archivo, lo decodifica y emite el resultado.

MORSE_GUI.PY

Importa QTextCursor, para escribir al final de la entrada.
Importa el receptor en un try/except. Si falla, la app sigue funcionando sin él, como ya hacías con codmorse.
Crea el panel dentro de la ventana y conecta sus dos señales.
_antes_de_escuchar: si la entrada tiene texto, pregunta si borrarlo. Después cambia automáticamente a modo Morse → Texto.
_recibir_morse: añade el Morse detectado al final de la ventana de entrada. Con «Traducir al escribir» activado se traduce en directo.
_recibir_bloque: igual, pero para un WAV, y lo pone en una línea nueva.
closeEvent: detiene la escucha al cerrar la ventana.

APP.PY

importa decodificar_wav.
la opción 3 pide la ruta de un WAV, lo decodifica y muestra el Morse y su traducción.

OTROS

morse_gui.spec: añade hiddenimports para que PyInstaller incluya QtMultimedia y los módulos nuevos, y NSMicrophoneUsageDescription para el permiso de micrófono en macOS.
test_decoder.py: 19 pruebas con audio sintético (ruido, velocidades, zumbido, cambio de velocidad…). Se ejecuta con python test_decoder.py y conviene lanzarlo si alguna vez tocas el decodificador.


Instalación para la versión Windows

Cambia poco respecto a la de Mac: no hay .app, ni info_plist, ni firma, y el resultado es una carpeta con un .exe. Hay dos archivos nuevos: morse_gui_windows.spec y construir_windows.bat. 
Qué cambia respecto a Mac
•	Qué genera: una carpeta dist\morse_gui con morse_gui.exe, no un .app.
•	Qué se quita: BUNDLE, info_plist y la firma con codesign, que son cosas de macOS.
•	Qué se mantiene: los hiddenimports de QtMultimedia y de los módulos nuevos, y upx=False.
•	Ventana: console=False evita la ventana negra de consola.
Pasos
1.	Instala Python 3 de 64 bits desde python.org, marcando «Add python.exe to PATH».
2.	Copia al mismo directorio estos archivos (crea un carpeta “morse”):
o	morse_gui.py, morse_receptor.py, morse_decoder.py y codmorse.py
o	morse_gui_windows.spec y construir_windows.bat
app.py y test_decoder.py no hacen falta.
3.	Haz doble clic en construir_windows.bat. Crea un entorno virtual, instala PyQt5 y pyinstaller y construye la aplicación.
4.	Resultado: dist\morse_gui\morse_gui.exe.
Si prefieres hacerlo a mano en cmd o PowerShell:
python -m venv venv
venv\Scripts\activate
pip install PyQt5 pyinstaller
python morse_gui.py
pyinstaller --noconfirm --clean morse_gui_windows.spec
El python morse_gui.py intermedio sirve para comprobar que todo funciona antes de empaquetar.
Para repartirlo
•	Entrega la carpeta entera, comprimida en un .zip: morse_gui.exe necesita los archivos que lo acompañan en dist\morse_gui.
•	Un solo .exe: puedes generarlo con pyinstaller --onefile --windowed morse_gui.py. Arranca más lento y los antivirus lo marcan como sospechoso con más frecuencia, así que te recomiendo la carpeta.
•	Instalador: si quieres un instalador clásico, Inno Setup puede empaquetar esa carpeta. Es opcional.
Qué esperar en otros equipos
•	SmartScreen: al abrirlo, Windows puede mostrar «Windows protegió su PC», porque el ejecutable no está firmado. Se abre con Más información → Ejecutar de todas formas. Para evitarlo harías falta un certificado de firma de código de pago, que no merece la pena para un uso entre aficionados.
•	Permiso de micrófono: en Configuración → Privacidad y seguridad → Micrófono, activa «Permitir que las aplicaciones de escritorio accedan al micrófono». Si no, el receptor mostrará el aviso rojo de «silencio absoluto».
•	Antivirus: si alguno bloquea el .exe, es un falso positivo habitual de los programas hechos con PyInstaller. Añade una excepción.
•	Si no arranca: pon console=True en el .spec y reconstruye. Verás el error en una ventana de consola. Si me lo pegas, lo resolvemos.
Puedes probar el resultado en un equipo sin Python instalado, para confirmar que no depende de nada de tu máquina de desarrollo.

