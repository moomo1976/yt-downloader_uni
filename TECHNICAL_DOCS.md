# YouTube Downloader Pro - Technical Documentation

## 🏗️ Architecture Overview

### Project Structure
```
YT_Downloader/
├── src/
│   ├── core/
│   │   └── downloader.py      # Core download logic
│   └── gui/
│       ├── simple_gui.py      # Main GUI implementation
│       └── modern_gui.py      # Alternative GUI (legacy)
├── Release/
│   ├── YouTube_Downloader_Pro.exe  # Built executable
│   ├── NÁVOD.md              # User documentation
│   └── RYCHLÝ_START.txt      # Quick start guide
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                # Project overview
```

### Core Components

#### 1. Main Entry Point (`main.py`)
```python
#!/usr/bin/env python3
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.simple_gui import main

if __name__ == "__main__":
    main()
```

#### 2. Video Downloader (`src/core/downloader.py`)
**Key Class**: `VideoDownloader`

**Main Methods**:
- `get_video_info(url)` - Extract video metadata
- `download_video_with_format(url, quality, format)` - Main download method  
- `_progress_hook(d)` - Progress callback handler
- `get_next_file_number()` - Auto-numbering system

**Features**:
- yt-dlp integration for YouTube downloads
- FFmpeg support for m3u8 streams
- Progress tracking with callbacks
- Format conversion (MP4, MP3, WEBM, AVI)
- Auto-numbered file naming (001-, 002-, etc.)

#### 3. GUI Interface (`src/gui/simple_gui.py`)
**Key Class**: `SimpleYTDownloader`

**GUI Framework**: CustomTkinter (modern dark theme)

**Main Components**:
- URL input section
- Quality/format selection
- Progress tracking with percentage display
- Folder management
- Real-time download status

## 🔧 Dependencies

### Runtime Dependencies
```txt
yt-dlp>=2023.7.6          # YouTube downloader
customtkinter>=5.2.0      # Modern GUI framework
Pillow>=10.0.0           # Image processing
requests>=2.31.0         # HTTP requests
```

### Build Dependencies
```txt
pyinstaller>=6.0.0       # Executable builder
setuptools>=68.0.0       # Package tools
```

### System Dependencies
- **FFmpeg** (optional) - For m3u8 stream processing
- **Windows 10/11** - Target platform

## 🏭 Build Process

### Development Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd YT_Downloader

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run in development
python main.py
```

### Production Build
```bash
# Build standalone executable
pyinstaller --onefile --windowed \
  --name "YouTube_Downloader_Pro" \
  --add-data "src;src" \
  --hidden-import=customtkinter \
  --hidden-import=tkinter \
  --hidden-import=PIL \
  --hidden-import=yt_dlp \
  --collect-all=customtkinter \
  --collect-all=yt_dlp \
  main.py
```

### Build Optimization
- **--onefile**: Single executable
- **--windowed**: No console window
- **--collect-all**: Include all package files
- **--hidden-import**: Explicit dependency inclusion

## 📊 Technical Specifications

### Performance Metrics
- **Executable Size**: ~37 MB (includes all dependencies)
- **Memory Usage**: ~50-150 MB during operation
- **Startup Time**: ~2-5 seconds (cold start)
- **Download Speed**: Limited by YouTube servers and internet connection

### Threading Architecture
```python
Main Thread (GUI)
├── User Interface Updates
├── Event Handling
└── Progress Display

Background Thread (Download)
├── yt-dlp Processing
├── File I/O Operations
└── Progress Callbacks → Main Thread
```

### Data Flow
```
User Input (URL) → Video Analysis → Quality Selection → Download Thread → Progress Updates → File Output
```

## 🔒 Security Considerations

### Input Validation
- URL format verification
- Path traversal protection
- File name sanitization
- Unicode encoding handling

### Network Security
- HTTPS only connections
- No credential storage
- Temporary file cleanup
- Safe download directory handling

### Code Security
- No eval() or exec() usage
- Subprocess sanitization
- Error handling without information disclosure

## 🐛 Error Handling

### Error Categories
1. **Network Errors** (403, 404, timeout)
2. **Format Errors** (unsupported quality/format)
3. **File System Errors** (permissions, disk space)
4. **Application Errors** (dependency issues, crashes)

### Error Recovery
```python
try:
    result = downloader.download_video(url, quality, format)
except Exception as e:
    # Log error, show user-friendly message
    self.show_error(f"Download failed: {str(e)}")
    # Reset UI state
    self.reset_download_state()
```

## 🔧 Configuration

### Default Settings
```python
DEFAULT_OUTPUT_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "YT_Downloads")
DEFAULT_QUALITY = "720p"
DEFAULT_FORMAT = "MP4"
PROGRESS_UPDATE_INTERVAL = 100  # milliseconds
```

### File Naming Convention
```python
# Pattern: {number:03d}-{title}.{extension}
# Example: 001-My Video Title.mp4
def get_filename(self, title, extension, number):
    safe_title = self.sanitize_filename(title)
    return f"{number:03d}-{safe_title}.{extension}"
```

## 📈 Performance Optimization

### GUI Responsiveness
- Threading for blocking operations
- Asynchronous progress updates
- Efficient UI update batching

### Memory Management
- Temporary file cleanup
- Progress callback optimization
- Large file streaming support

### Download Optimization
- Format selection based on availability
- Adaptive quality selection
- Resume capability (yt-dlp feature)

## 🧪 Testing Strategy

### Unit Testing
```python
# Test core downloader functionality
def test_video_info_extraction():
    downloader = VideoDownloader()
    info = downloader.get_video_info(TEST_URL)
    assert info['title'] is not None
    assert len(info['formats']) > 0

# Test file naming
def test_file_numbering():
    downloader = VideoDownloader()
    num = downloader.get_next_file_number()
    assert isinstance(num, int)
    assert num > 0
```

### Integration Testing
- GUI interaction testing
- Download process validation
- Error scenario handling
- Cross-platform compatibility

## 🚀 Deployment

### Distribution Package
```
Release/
├── YouTube_Downloader_Pro.exe  # Main executable (37MB)
├── NÁVOD.md                   # User documentation
├── RYCHLÝ_START.txt           # Quick start guide
└── README.txt                 # Basic info
```

### System Requirements
- **OS**: Windows 10 (1903+) or Windows 11
- **Architecture**: x64
- **RAM**: Minimum 512MB available
- **Disk**: 50MB free space
- **Network**: Internet connection required

## 📝 Code Quality Standards

### Python Style
- PEP 8 compliance
- Type hints where applicable
- Docstring documentation
- Error handling best practices

### GUI Standards
- Responsive design
- Accessibility considerations
- Consistent theming
- User feedback mechanisms

## 🔮 Future Enhancements

### Planned Features
- [ ] Playlist download support
- [ ] Batch URL processing
- [ ] Download queue management
- [ ] Custom output filename templates
- [ ] Subtitle download
- [ ] Quality auto-selection based on connection speed

### Technical Improvements
- [ ] Async/await GUI implementation
- [ ] Plugin system for extractors
- [ ] Configuration file support
- [ ] Logging system
- [ ] Update mechanism
- [ ] Multi-language support

## 📚 API Reference

### VideoDownloader Class
```python
class VideoDownloader:
    def __init__(self, output_path: str = None)
    def get_video_info(self, url: str) -> Dict
    def download_video_with_format(self, url: str, quality: str, 
                                   format_choice: str, 
                                   progress_callback: Callable = None) -> Dict
    def get_next_file_number(self) -> int
    def check_ffmpeg(self) -> bool
```

### SimpleYTDownloader Class
```python
class SimpleYTDownloader:
    def __init__(self)
    def setup_ui(self)
    def start_download(self)
    def browse_folder(self)
    def _progress_callback(self, progress_info: Dict)
```

---

**Documentation Version**: 1.0  
**Last Updated**: September 2024  
**Maintainer**: Claude Code Assistant