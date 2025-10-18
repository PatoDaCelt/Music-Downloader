import yt_dlp
import os

def download_music(url, carpeta="Music_test"):
    try:
        if not os.path.exist(carpeta):
            os.makedirs(carpeta)
        opciones = {
            'format' : 'bestaudio/best', #Descargue el audio en la mehor calidad disponible
            'outtmpl' : f'(carpeta)/%(title)s.%(ext)s' #Los archivos se guarden con el nombre del video
        }
        print("Descargando audio del video...")
        
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
            print("Descarga completa!!")
            
    except Exception as e:
        print(f"Ocurrio un error: {e}")

if __name__ == "__main__":
    url = input("Ingrese la url del video: ")
    download_music(url)