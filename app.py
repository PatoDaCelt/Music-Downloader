from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        # Opciones para descargar y convertir a mp3
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': 'ffmpeg',  # usa ffmpeg del sistema
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            filename = f"{title}.mp3"
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        # A veces yt_dlp no borra el archivo .webm original, puedes limpiarlo:
        for ext in ('.webm', '.m4a'):
            oldfile = os.path.join(DOWNLOAD_FOLDER, f"{title}{ext}")
            if os.path.exists(oldfile):
                os.remove(oldfile)

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return f"Error al procesar el video: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)