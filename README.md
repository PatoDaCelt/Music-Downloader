# Music-Downloader
Downloader en web que pasa el link del video de Youtube a formato .mp3 para descargarlo.


# Diagrama de flujo
1- El Usuario pega una URL en la página web y hace clic en "Descargar".

2- Flask recibe la URL en la ruta /download.

3- La librería yt-dlp descarga el archivo de audio original (.webm).

4- Usando el programa FFmpeg se convierte el archivo .webm a .mp3.

5- Flask envía el archivo .mp3 al usuario.

6- Flask (Post-Petición): Borra los archivos temporales (.webm y .mp3) del servidor.