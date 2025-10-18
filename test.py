import subprocess
import os

def convert_webm_to_mp3_ffmpeg(input_file, output_file):
    """Convierte un archivo WEBM a MP3 usando FFmpeg."""
    # Asegúrate de que el archivo de salida tenga la extensión .mp3
    base_name = os.path.splitext(input_file)[0]
    if not output_file.lower().endswith('.mp3'):
        output_file = f"{base_name}.mp3"

    # Comando para extraer solo el audio y guardarlo como MP3
    # -i indica el archivo de entrada
    # -vn significa que no se procesará video
    # -acodec libmp3lame es el códec para MP3
    # -ab es el bitrate de audio (p.ej., 192k)
    # output_file es el nombre del archivo de salida
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vn',
        '-acodec', 'libmp3lame',
        '-ab', '192k',
        output_file
    ]
    subprocess.call(command)

# Ejemplo de uso
convert_webm_to_mp3_ffmpeg('downloads/50 Cent - In Da Club (HQ).webm', '50 Cent - In Da Club.mp3')
