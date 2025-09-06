# Systém ověřování závislostí

YouTube Downloader Pro nyní obsahuje automatickou kontrolu všech potřebných komponent při spuštění.

## 🔍 Co se kontroluje

### Systémové komponenty
- **FFmpeg** - požadováno pro stahování M3U8 streamů a konverzi videí
  - Kontroluje se dostupnost příkazu `ffmpeg -version`
  - Při absenci se zobrazí návod na instalaci

### Python balíčky
- **yt-dlp** - hlavní knihovna pro stahování videí
- **customtkinter** - moderní GUI framework
- **Pillow** - zpracování obrázků
- **requests** - HTTP požadavky

## 🚀 Použití

### Automatická kontrola při spuštění
Program automaticky kontroluje závislosti při každém spuštění GUI aplikace. Pokud něco chybí, zobrazí se varovné okno s instrukcemi.

### Ruční kontrola
```bash
# Spuštění kontroly ze složky projektu
python check_dependencies.py
```

### Menu v aplikaci
V GUI aplikaci najdete v menu "Nástroje" > "🔍 Kontrola závislostí" možnost ruční kontroly.

## 📋 Výstup kontroly

### Všechno v pořádku
```
✅ SYSTÉMOVÉ KOMPONENTY:
   ✅ ffmpeg je dostupný

✅ PYTHON BALÍČKY:
   ✅ yt-dlp je dostupný
   ✅ customtkinter je dostupný
   ✅ Pillow je dostupný
   ✅ requests je dostupný

✅ Všechny komponenty jsou v pořádku!
```

### Chybějící komponenty
```
❌ SYSTÉMOVÉ KOMPONENTY:
   ❌ ffmpeg nebyl nalezen v PATH

✅ PYTHON BALÍČKY:
   ✅ yt-dlp je dostupný
   ❌ customtkinter není nainstalován

💡 RYCHLÁ INSTALACE:
   pip install customtkinter

🔧 ŘEŠENÍ FFmpeg:
   Stáhněte z https://ffmpeg.org/download.html
```

## 🛠️ Řešení problémů

### Chybějící Python balíčky
```bash
pip install yt-dlp customtkinter Pillow requests
```

### Chybějící FFmpeg
1. **Windows**: Stáhněte z https://ffmpeg.org/download.html a přidejte do PATH
2. **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) nebo `sudo yum install ffmpeg` (RHEL/CentOS)
3. **macOS**: `brew install ffmpeg`

### Problémy s kódováním (Windows)
Pokud vidíte chyby s Unicode znaky, spusťte:
```cmd
set PYTHONIOENCODING=utf-8
python check_dependencies.py
```

## 🔧 Technické detaily

### Struktura kódu
- `src/core/dependency_checker.py` - hlavní třída `DependencyChecker`
- `check_dependencies.py` - samostatný skript pro kontrolu
- Integrace v `src/gui/simple_gui.py` při spuštění aplikace

### API
```python
from core.dependency_checker import DependencyChecker

checker = DependencyChecker()
results = checker.check_all_dependencies()

if results['all_ok']:
    print("Vše v pořádku!")
else:
    print("Chybí:", results['critical_missing'])
```

## 🔄 Co se stane při chybách

1. **Chybějící FFmpeg**: Aplikace funguje, ale M3U8 streamy nejdou stáhnout
2. **Chybějící Python balíčky**: Aplikace se nemusí spustit vůbec
3. **Varovné okno**: Zobrazí se při spuštění, ale aplikace pokračuje
4. **Log výpis**: Všechny chyby se logují pro diagnostiku

## 💡 Tipy

- Spusťte kontrolu před každou důležitou prací
- V případě problémů restartujte aplikaci po instalaci komponent
- Zkontrolujte PATH proměnnou pro systémové nástroje
- Používejte virtuální prostředí pro Python balíčky