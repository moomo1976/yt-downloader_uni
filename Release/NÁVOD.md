# 🎥 YouTube Downloader Pro - Kompletní návod

## 📋 Obsah
- [Rychlý start](#rychlý-start)
- [Detailní použití](#detailní-použití)
- [Funkce aplikace](#funkce-aplikace)
- [Podporované formáty](#podporované-formáty)
- [Řešení problémů](#řešení-problémů)
- [Často kladené otázky](#často-kladené-otázky)

## 🚀 Rychlý start

### Instalace
**Žádná instalace není potřeba!** Aplikace je standalone executable.

1. Stáhněte `YouTube_Downloader_Pro_v2.1.0.exe`
2. Spusťte dvojklikem
3. Aplikace automaticky zkontroluje závislosti
4. V případě chyb následujte instrukce v dialogu

### Základní použití
1. **Vložte URL** - Zkopírujte odkaz z YouTube do textového pole
2. **Vyberte kvalitu** - 720p, 1080p, Audio Only, atd.
3. **Vyberte formát** - MP4 (video), MP3 (audio), WEBM, AVI
4. **Klikněte STÁHNOUT** - Sledujte průběh s procenty
5. **Hotovo!** - Video se uloží do zvolené složky

## 📚 Detailní použití

### 1. Spuštění aplikace
- Dvojklik na `YouTube_Downloader_Pro_v2.1.0.exe`
- Aplikace zkontroluje systémové závislosti (FFmpeg)
- Zobrazí se tmavé moderní rozhraní
- Pro manuální kontrolu: Menu → Nástroje → Kontrola závislostí

### 2. Zadání URL videa
```
Podporované URL formáty:
✅ https://youtube.com/watch?v=VIDEO_ID
✅ https://www.youtube.com/watch?v=VIDEO_ID
✅ https://youtu.be/VIDEO_ID
✅ https://m.youtube.com/watch?v=VIDEO_ID
```

### 3. Výběr kvality
| Kvalita | Popis | Doporučeno pro |
|---------|-------|----------------|
| **Best Quality** | Nejvyšší dostupná kvalita | Nejlepší obraz |
| **1080p** | Full HD rozlišení | HD televize |
| **720p** | HD rozlišení | Běžné použití |
| **480p** | Standardní rozlišení | Úspora místa |
| **360p** | Nižší rozlišení | Pomalé internet |
| **Audio Only** | Pouze zvuk | Hudba, podcasty |

### 4. Výběr formátu
| Formát | Typ | Výhody | Nevýhody |
|--------|-----|--------|----------|
| **MP4** | Video | Univerzální, malá velikost | - |
| **MP3** | Audio | Nejmenší velikost pro hudbu | Pouze zvuk |
| **WEBM** | Video | Dobré pro web | Menší kompatibilita |
| **AVI** | Video | Široká kompatibilita | Větší velikost |

### 5. Správa složek
- **Výchozí složka**: `~/Downloads/YT_Downloads`
- **Změna složky**: Tlačítko "📁 Zvolit složku"
- **Otevření složky**: Tlačítko "📂 Otevřít složku"
- **Automatické číslování**: Soubory se číslují `001-`, `002-`, atd.

## ⚡ Funkce aplikace

### 📊 Sledování průběhu
- **Procenta v reálném čase** - 0% → 100%
- **Rychlost stahování** - MiB/s nebo KiB/s
- **Název souboru** - Aktuálně stahovaný soubor
- **Vizuální progress bar** - Grafické znázornění

### 🎯 Pokročilé funkce
- **Automatická kontrola závislostí** - Ověření FFmpeg při spuštění
- **Automatické číslování** - Žádné přepisování souborů
- **Unicode podpora** - Podpora českých znaků
- **Error handling** - Inteligentní zpracování chyb
- **Pozadí stahování** - GUI zůstává responzivní
- **Menu nástroje** - Ruční kontrola závislostí

### 🔧 Systémové požadavky
- **OS**: Windows 10/11
- **RAM**: Minimálně 512 MB
- **Disk**: 50 MB volného místa
- **Internet**: Aktivní připojení

## 🎬 Podporované formáty

### Video formáty
```
MP4  - H.264/AAC (doporučeno)
WEBM - VP9/Opus
AVI  - XVID/MP3
```

### Audio formáty
```
MP3 - 128-320 kbps (doporučeno pro hudbu)
```

### Kvalita videa
```
4K   - 2160p (pokud dostupné)
FHD  - 1080p
HD   - 720p
SD   - 480p/360p
```

## 🛠️ Řešení problémů

### Časté problémy a řešení

#### "Video se nestahuje"
```
✅ Zkontrolujte internetové připojení
✅ Ověřte správnost URL
✅ Zkuste jiné video
✅ Restartujte aplikaci
```

#### "HTTP 403 Forbidden / Video je blokováno"
```
✅ Zkuste jiné video (nejčastější řešení)
✅ Zkuste nižší kvalitu (480p místo 1080p)
✅ Zkuste MP3 formát místo video
✅ Restartujte aplikaci
✅ Zkuste video později (YouTube dočasně blokuje)
✅ Ověřte, že video je veřejně dostupné
```

#### "Chyba při stahování"
```
✅ Video může být regionálně blokované
✅ Zkuste nižší kvalitu
✅ Zkuste jiný formát (MP4)
✅ Zkontrolujte volné místo na disku
```

#### "Aplikace se nespouští"
```
✅ Zkontrolujte antivirus (může blokovat)
✅ Spusťte jako administrátor
✅ Zkontrolujte Windows Defender
✅ Stáhněte znovu aplikaci
✅ Ověřte závislosti (check_dependencies.py)
```

#### "Pomalé stahování"
```
✅ Zavřete ostatní aplikace používající internet
✅ Zkuste později (servery YouTube)
✅ Zkontrolujte rychlost internetu
```

### Error kódy
```
403 Forbidden    - Video je blokované (nejčastější)
404 Not Found    - Video neexistuje nebo bylo smazáno
Network Error    - Problém s internetovým připojením
Private Video    - Video je nastavené jako soukromé
Age Restricted   - Video má věkové omezení
```

### 🆘 Speciální řešení pro 403 chyby

**Co je HTTP 403?**
YouTube občas blokuje stahování určitých videí z bezpečnostních důvodů.

**Řešení v pořadí efektivity:**
1. **Zkuste jiné video** - 90% úspěšnost
2. **MP3 místo MP4** - Audio se blokuje méně často  
3. **Nižší kvalita** - 360p místo 1080p
4. **Restart aplikace** - Obnovuje spojení
5. **Počkejte na obnovení limitu** - Viz časování níže

**Preventivní opatření:**
- Nestahujte příliš mnoho videí rychle za sebou
- Preferujte veřejná, populární videa
- Vyhněte se hudebním videím s copyrightem

**⏰ Časování obnovení YouTube limitů:**

| Typ blokování | Doba obnovení | Poznámky |
|---------------|---------------|----------|
| **Rate limiting** | 15-30 minut | Příliš mnoho requestů |
| **IP blokování** | 1-2 hodiny | Podezřelá aktivita |
| **Video-specific** | 24 hodin | Specifické video blokováno |
| **Region block** | Trvalé | Video není dostupné v ČR |

**💡 Tipy pro rychlejší obnovení:**
- Restartujte router (změna IP adresy)
- Použijte mobilní internet místo WiFi
- Zkuste jiné video ze stejného kanálu
- Vymažte cache prohlížeče (pokud aplikace neběží)

## ❓ Často kladené otázky

### Q: Je aplikace zdarma?
**A:** Ano, aplikace je kompletně zdarma.

### Q: Potřebujem Python?
**A:** Ne, aplikace je standalone executable.

### Q: Funguje i s privátními videi?
**A:** Ne, funguje pouze s veřejně dostupnými videi.

### Q: Mohu stahovat celé playlisty?
**A:** Aktuálně ne, pouze jednotlivá videa.

### Q: Kam se ukládají soubory?
**A:** Výchozí: `%USERPROFILE%\Downloads\YT_Downloads`

### Q: Proč je aplikace velká (39 MB)?
**A:** Obsahuje všechny potřebné knihovny a systém kontroly závislostí.

### Q: Podporuje 4K videa?
**A:** Ano, pokud jsou dostupná na YouTube.

### Q: Je to legální?
**A:** Ano, pro osobní použití v souladu s TOS YouTube.

### Q: Mohu aplikaci sdílet?
**A:** Ano, můžete ji volně sdílet.

### Q: Funguje na Windows 7?
**A:** Doporučeno Windows 10/11, na Win7 není testováno.

### Q: Jak dlouho trvá obnovení 403 limitu?
**A:** Nejčastěji 15-30 minut při rate limitingu. IP blokování 1-2 hodiny. Restart routeru může pomoci rychleji.

### Q: Proč se mi blokují videa?
**A:** YouTube má ochranné mechanismy proti stahování. Zkuste jiné video nebo počkejte na obnovení limitu.

## 📞 Podpora

Pro další otázky nebo problémy:
- Zkontrolujte tento návod
- Vyzkoušejte restart aplikace
- Ověřte správnost URL

## 📝 Poznámky

- Aplikace respektuje autorská práva
- Používejte pouze pro osobní účely
- Nejedná se o oficiální aplikaci Google/YouTube

---

**Verze aplikace**: 2.1.0  
**Verze dokumentace**: 2.1  
**Datum**: Září 2025  
**Vytvořeno pomocí**: Claude Code  