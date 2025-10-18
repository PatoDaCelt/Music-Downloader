import os
import subprocess
from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp

# Códigos de colores para mensajes en terminal
RE = "\033[31m"
GR = "\033[32m"
BU = "\033[34m"
RS = "\033[0m" #RESET

# --- Configuración de la Aplicación ---
app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads" # Define el nombre de la carpeta donde se guardarán temporalmente los archivos.

# Crear la carpeta de descargas si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# --- Rutas de la Aplicación ---
# RUTA PRINCIPAL
@app.route('/')
def index():
    """Muestra la página principal"""
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    """
    Gestiona la descarga y conversión del audio.
    """
    url = request.form['url'] #Obtiene la URL poporcionada
    if not url:
        return render_template('index.html', mensaje="Por favor, introduce un enlace de YouTube.")

    try:
        #Diccionario de opciones para yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best', #Descarga el mejor audio posible.
            'outtmpl': os.path.join(DOWNLOAD_FOLDER,'%(title)s.%(ext)s'), # El nombre del archivo se basará en el título del video.
            'noplaylist': True, #Si la URL es de una lista de reproducción, solo descargará el video individual.
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #Extrae toda la información del video
            info = ydl.extract_info(url, download=True) 
            title = info.get('title', 'audio_descargado')
            ext = info.get('ext', 'webm')
            
            # Ruta completa del archivo original y del archivo final en MP3.
            original_filename_without_ext = ydl.prepare_filename(info).replace(f'.{ext}', '')
            original_filepath = f"{original_filename_without_ext}.{ext}"
            mp3_filepath = f"{original_filename_without_ext}.mp3"
            
        #Conversión a MP3
        print(f"Convirtiendo {RE}'{original_filepath}'{RS} a {BU}'{mp3_filepath}'{RS}...")
        command = [
            'ffmpeg',
            '-i', original_filepath,  # Archivo de entrada
            '-vn',                    # No procesar video
            '-acodec', 'libmp3lame',  # Codec de audio MP3
            '-ab', '192k',            # Bitrate de audio
            '-y',                     # Sobrescribir si el archivo de salida ya existe
            mp3_filepath              # Archivo de salida
        ]
        
        # Ejecutamos el comando de FFmpeg.
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{GR}Conversión completada.{RS}")

        # Preparamos una función para que borre AMBOS archivos después de que la descarga se complete.
        @after_this_request
        def cleanup(response):
            try:
                print(f"Borrando archivo original: {original_filepath}")
                os.remove(original_filepath)
                print(f"Borrando archivo MP3: {mp3_filepath}")
                os.remove(mp3_filepath)
            except OSError as e:
                app.logger.error(f"Error al borrar el archivo: {e}")
            return response

        # Enviamos el archivo MP3 recién creado al usuario.
        return send_file(mp3_filepath, as_attachment=True)

    except subprocess.CalledProcessError as e:
        # Captura errores específicos de FFmpeg.
        error_message = e.stderr.decode('utf-8', errors='ignore')
        return f"Error durante la conversión con FFmpeg: <pre>{error_message}</pre>", 500
    except Exception as e:
        # Captura cualquier otro error (como un URL inválido).
        return f"Ocurrió un error: {str(e)}", 500

# --- Inicio de la Aplicación ---
if __name__ == '__main__':
    app.run(debug=True)