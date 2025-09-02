import subprocess
import sys
import os
import tkinter as tk
from tkinter import simpledialog, filedialog

# Funkce pro kontrolu a instalaci balíčku
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Balíček {package} není nainstalován. Instalace...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Funkce pro kontrolu ffmpeg
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("ffmpeg je nainstalován.")
    except FileNotFoundError:
        print("Chyba: ffmpeg není nainstalován. Instalace je nutná pro slučování videa a audia.")
        print("Zkuste nainstalovat ffmpeg ručně nebo pomocí winget: 'winget install ffmpeg'.")
        sys.exit(1)

# Funkce pro stažení obsahu přes yt-dlp
def download_playlist_with_yt_dlp(url, output_path):
    try:
        subprocess.run([
            "yt-dlp",
            "--yes-playlist",  # Povolit stahování celého playlistu
            "-o", f"{output_path}/%(playlist_index)s-%(title)s.%(ext)s",  # Ukládání s indexem
            url
        ], check=True)
        print(f"Playlist {url} úspěšně stažen do složky: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Chyba při stahování playlistu pomocí yt-dlp: {e}")

# Zkontrolujte a nainstalujte požadované knihovny
install_and_import("yt-dlp")
check_ffmpeg()

from yt_dlp import YoutubeDL

# Vyber složku pro ukládání videí
root = tk.Tk()
root.withdraw()
download_path = filedialog.askdirectory(title="Vyberte složku pro ukládání videí")
if not download_path:
    print("Nebyla vybrána žádná složka. Program se ukončuje.")
    sys.exit(0)

# Stahování playlistů nebo jednotlivých videí na základě uživatelského vstupu
while True:
    link = simpledialog.askstring("Vložit odkaz", "Zadejte odkaz na video, playlist nebo m3u8 (napište 'konec' pro ukončení):")
    if not link or link.lower().strip() == "konec":
        print("Program ukončen.")
        break

    try:
        if "list=" in link:  # Rozpoznání playlistu podle parametru 'list'
            download_playlist_with_yt_dlp(link.strip(), download_path)
        elif link.endswith(".m3u8"):
            output_file = f"{download_path}/stream.mp4"
            download_with_ffmpeg(link.strip(), output_file)
        else:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': f'{download_path}/%(title)s.%(ext)s'
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([link.strip()])
                print(f"Video {link} úspěšně staženo.")
    except Exception as e:
        print(f"Stažení selhalo: {e}")

print("Stažení dokončeno!")
