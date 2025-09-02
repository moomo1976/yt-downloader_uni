import subprocess
import sys
import os
import tkinter as tk
from tkinter import simpledialog

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

# Funkce pro stažení obsahu přes ffmpeg
def download_with_ffmpeg(url, output_path):
    try:
        subprocess.run([
            "ffmpeg",
            "-http_persistent", "0",  # Zakázat persistentní spojení
            "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  # Nastavit User Agent
            "-i", url,
            "-c", "copy",
            output_path
        ], check=True)
        print(f"Video úspěšně staženo do souboru: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Chyba při stahování videa pomocí ffmpeg: {e}")

# Funkce pro stažení obsahu přes yt-dlp
def download_with_yt_dlp(url, output_path):
    try:
        subprocess.run(["yt-dlp", "-o", output_path, url], check=True)
        print(f"Video úspěšně staženo do souboru: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Chyba při stahování videa pomocí yt-dlp: {e}")

# Zkontrolujte a nainstalujte požadované knihovny
install_and_import("yt-dlp")
check_ffmpeg()

from yt_dlp import YoutubeDL

# Cesta ke stažení videí
download_path = "E:/webREBEL/Skool-Amelin/"

# Funkce pro zjištění dalšího čísla souboru
def get_next_file_number(path):
    existing_files = [f for f in os.listdir(path) if f.endswith(".mp4")]
    numbers = []
    for file in existing_files:
        try:
            number = int(file.split('-')[0])
            numbers.append(number)
        except (ValueError, IndexError):
            continue
    return max(numbers, default=0) + 1

# Nastavení pro stažení videí v nejvyšší možné kvalitě
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # Nejlepší video a audio dostupné kvality
    'merge_output_format': 'mp4',
    'outtmpl': f'{download_path}/%(title)s.%(ext)s'
}

# Inicializace Tkinter
root = tk.Tk()
root.withdraw()

# Stahování videí na základě uživatelského vstupu
while True:
    link = simpledialog.askstring("Vložit odkaz", "Zadejte odkaz na video nebo m3u8 (napište 'konec' pro ukončení):")
    if not link or link.lower().strip() == "konec":
        print("Program ukončen.")
        break

    try:
        if link.endswith(".m3u8"):
            next_number = get_next_file_number(download_path)
            output_file = f"{download_path}/{next_number:03d}-stream.mp4"
            download_with_ffmpeg(link.strip(), output_file)
        else:
            next_number = get_next_file_number(download_path)
            ydl_opts['outtmpl'] = f'{download_path}/{next_number:03d}-%(title)s.%(ext)s'
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([link.strip()])
                print(f"Video {link} úspěšně staženo.")
    except Exception as e:
        print(f"Stažení videa {link} selhalo: {e}")

print("Stažení dokončeno!")
