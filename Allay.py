import os
import threading
import flet as ft
import yt_dlp

def main(page: ft.Page):
    page.title = "Allay - Descargador de Música"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 450
    page.window_height = 550

    titulo = ft.Text("Allay Music", size=24, weight=ft.FontWeight.BOLD)
    
    url_input = ft.TextField(
        label="Pega el enlace de YouTube o Playlist aquí...", 
        width=350,
        border_radius=10
    )
    
    status_text = ft.Text("Esperando enlace...", size=14, color="grey")
    progress_ring = ft.ProgressRing(visible=False, width=30, height=30)

    def iniciar_descarga(e):
        url = url_input.value.strip()
        if not url:
            status_text.value = "¡Por favor, pega un enlace válido!"
            status_text.color = "red"
            page.update()
            return

        btn_download.disabled = True
        progress_ring.visible = True
        status_text.value = "Iniciando descarga..."
        status_text.color = "blue"
        page.update()

        threading.Thread(target=proteger_descarga, args=(url,)).start()

    def proteger_descarga(url):
        try:
            if page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
                output_dir = os.path.join(os.path.expanduser("~"), "storage", "shared", "Music", "Allay_Music")
            else:
                output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "Allay_Downloads")
            
            os.makedirs(output_dir, exist_ok=True)

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }, {
                    'key': 'EmbedThumbnail',
                }, {
                    'key': 'FFmpegMetadata',
                }],
                'addmetadata': True,
                'writethumbnail': True,
                'progress_hooks': [hook_progreso],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_text.value = f"¡Descarga completada!\nGuardado en la carpeta de música."
            status_text.color = "green"
        except Exception as ex:
            status_text.value = f"Error: {str(ex)}"
            status_text.color = "red"
        finally:
            btn_download.disabled = False
            progress_ring.visible = False
            page.update()

    def hook_progreso(d):
        if d['status'] == 'downloading':
            status_text.value = f"Descargando: {d.get('_percent_str', '0%')} completado"
            page.update()
        elif d['status'] == 'finished':
            status_text.value = "Procesando audio, carátula y metadatos..."
            page.update()

    btn_download = ft.Button(
        content=ft.Text("Descargar MP3 (320kbps)"), 
        on_click=iniciar_descarga,
    )

    page.add(
        titulo,
        ft.Container(height=15),
        url_input,
        ft.Container(height=10),
        btn_download,
        ft.Container(height=15),
        progress_ring,
        ft.Container(height=10),
        status_text
    )

if __name__ == "__main__":
    ft.run(main)