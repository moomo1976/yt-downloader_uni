# 🎥 YouTube Downloader Pro v2.1.0

Modern YouTube video downloader with automatic dependency checking, intuitive GUI, quality selection, and progress tracking.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🆕 **New in v2.1.0:**
- 🔍 **Automatic Dependency Checking** - Verifies FFmpeg and Python packages on startup
- ⚠️ **Smart Error Handling** - Warning dialogs with installation instructions
- 🛠️ **Tools Menu** - Manual dependency check and diagnostics
- 📋 **Standalone Diagnostics** - `check_dependencies.py` script for troubleshooting

### 🎯 **Core Features:**
- 🎨 **Modern Dark Theme UI** - Built with CustomTkinter
- 📺 **Multiple Video Sources** - YouTube videos, playlists, and m3u8 streams  
- 🎯 **Quality Selection** - Choose from 144p to 4K or audio-only
- 📊 **Real-time Progress** - Download progress with speed indicators
- 📁 **Custom Output** - Choose your download location
- 🔢 **Auto-numbering** - Sequential file numbering (001-, 002-, etc.)
- ⚡ **Multi-threading** - Non-blocking UI during downloads

## 🚀 Quick Start

### Option 1: Download Executable (Recommended)

1. Go to [Releases](https://github.com/moomo1976/yt-downloader_uni/releases)
2. Download `YouTube_Downloader_Pro_v2.1.0.exe` (~39MB)
3. Run the executable - no installation required!
4. Application automatically checks dependencies on first run

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/moomo1976/yt-downloader_uni.git
cd yt-downloader_uni

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# For dependency checking
python check_dependencies.py
```

## 📋 Requirements

- **Python**: 3.8 or higher (for source installation)
- **FFmpeg**: Required for m3u8 streams and video processing (auto-detected in v2.1.0)
- **Operating System**: Windows, macOS, or Linux

> 💡 **New in v2.1.0:** Application automatically checks for missing dependencies and provides installation instructions!

### Installing FFmpeg

**Windows:**
```bash
winget install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 🎮 Usage

1. **Launch** the application (dependency check runs automatically)
2. **Paste** a YouTube URL or m3u8 stream link
3. **Select Quality** from the dropdown menu (720p, 1080p, Audio Only, etc.)
4. **Choose Format** (MP4, MP3, WEBM, AVI)
5. **Choose Output Folder** (optional)
6. **Click Download** and watch the real-time progress!

### 🔧 **Troubleshooting (New in v2.1.0):**
- Missing dependencies? Check **Tools → Dependency Check**
- Run `check_dependencies.py` for detailed diagnostics
- Application shows warning dialogs with installation instructions

### Supported URL Types

- ✅ YouTube videos: `https://youtube.com/watch?v=...`
- ✅ YouTube playlists: `https://youtube.com/playlist?list=...`
- ✅ m3u8 streams: `https://example.com/stream.m3u8`
- ✅ Other video platforms supported by yt-dlp

## 🛠️ Development

### Project Structure

```
yt-downloader-pro/
├── src/
│   ├── gui/              # User interface
│   │   └── modern_gui.py
│   ├── core/             # Download logic
│   │   └── downloader.py
│   └── utils/            # Helper functions
├── assets/               # Icons and resources
├── tests/                # Unit tests
├── .github/workflows/    # CI/CD
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── setup.py            # Package setup
```

### Building from Source

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "YT-Downloader-Pro" main.py
```

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/yt-downloader_uni.git
cd yt-downloader_uni

# Install in development mode
pip install -e .

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful video downloader
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern Tkinter UI
- [FFmpeg](https://ffmpeg.org/) - Video processing toolkit

## 🐛 Bug Reports

Found a bug? Please create an [issue](https://github.com/moomo1976/yt-downloader_uni/issues) with:

- OS and Python version
- Error message (if any)
- Steps to reproduce
- Example URL (if applicable)

## 📞 Support

- 💬 [GitHub Discussions](https://github.com/moomo1976/yt-downloader_uni/discussions)
- 🐛 [Issue Tracker](https://github.com/moomo1976/yt-downloader_uni/issues)

---

⭐ **Star this repo if you find it useful!**