"""
Modern YouTube Downloader Core Module
Handles video downloading with quality selection and progress tracking
"""
import os
import subprocess
import sys
from typing import Optional, Callable, Dict, List
from yt_dlp import YoutubeDL


class VideoDownloader:
    def __init__(self, output_path: str = None):
        self.output_path = output_path or os.path.join(os.path.expanduser("~"), "Downloads", "YT_Downloads")
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        os.makedirs(self.output_path, exist_ok=True)
    
    def check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False
    
    def get_video_info(self, url: str) -> Dict:
        """Get video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'formats': self._extract_formats(info.get('formats', []))
                }
            except Exception as e:
                return {'error': str(e)}
    
    def _extract_formats(self, formats: List) -> List[Dict]:
        """Extract available video qualities"""
        quality_formats = []
        seen_heights = set()
        
        for fmt in formats:
            if fmt.get('vcodec') != 'none' and fmt.get('height'):
                height = fmt.get('height')
                if height not in seen_heights:
                    quality_formats.append({
                        'format_id': fmt.get('format_id'),
                        'quality': f"{height}p",
                        'ext': fmt.get('ext', 'mp4'),
                        'filesize': fmt.get('filesize')
                    })
                    seen_heights.add(height)
        
        # Add audio-only option
        quality_formats.append({
            'format_id': 'bestaudio',
            'quality': 'Audio Only (MP3)',
            'ext': 'mp3',
            'filesize': None
        })
        
        return sorted(quality_formats, key=lambda x: int(x['quality'].replace('p', '').replace('Audio Only (MP3)', '0')), reverse=True)
    
    def get_next_file_number(self) -> int:
        """Get next sequential file number"""
        existing_files = [f for f in os.listdir(self.output_path) 
                         if f.endswith(('.mp4', '.mp3', '.webm'))]
        numbers = []
        
        for file in existing_files:
            try:
                number = int(file.split('-')[0])
                numbers.append(number)
            except (ValueError, IndexError):
                continue
        
        return max(numbers, default=0) + 1
    
    def download_video(self, url: str, quality: str = 'best', 
                      progress_callback: Optional[Callable] = None) -> Dict:
        """Download video with specified quality"""
        return self.download_video_with_format(url, quality, 'MP4', progress_callback)
    
    def download_video_with_format(self, url: str, quality: str = 'best', 
                                 format_choice: str = 'MP4',
                                 progress_callback: Optional[Callable] = None) -> Dict:
        """Download video with specified quality and format"""
        try:
            # Handle m3u8 streams with ffmpeg
            if url.endswith('.m3u8'):
                return self._download_m3u8(url, progress_callback)
            
            # Regular YouTube/video download
            return self._download_with_ytdlp(url, quality, format_choice, progress_callback)
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _download_m3u8(self, url: str, progress_callback: Optional[Callable] = None) -> Dict:
        """Download m3u8 stream using ffmpeg"""
        if not self.check_ffmpeg():
            return {'success': False, 'error': 'FFmpeg not found'}
        
        next_number = self.get_next_file_number()
        output_file = os.path.join(self.output_path, f"{next_number:03d}-stream.mp4")
        
        try:
            if progress_callback:
                progress_callback({'status': 'downloading', 'filename': os.path.basename(output_file)})
            
            subprocess.run([
                "ffmpeg", "-y",
                "-http_persistent", "0",
                "-user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "-i", url,
                "-c", "copy",
                output_file
            ], check=True, capture_output=True)
            
            if progress_callback:
                progress_callback({'status': 'finished', 'filename': os.path.basename(output_file)})
            
            return {'success': True, 'filename': output_file}
            
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': f'FFmpeg error: {e}'}
    
    def _download_with_ytdlp(self, url: str, quality: str, format_choice: str = 'MP4', 
                           progress_callback: Optional[Callable] = None) -> Dict:
        """Download using yt-dlp with format selection"""
        next_number = self.get_next_file_number()
        
        # Configure format based on quality selection
        if quality == 'bestaudio':
            format_selector = 'bestaudio/best'
        else:
            if quality == 'best':
                format_selector = 'bestvideo+bestaudio/best'
            else:
                height = quality.replace("p", "")
                format_selector = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
        
        # Configure output format based on user choice
        format_lower = format_choice.lower()
        if format_lower == 'mp3' or quality == 'bestaudio':
            merge_format = 'mp3'
            format_selector = 'bestaudio/best'
        elif format_lower == 'webm':
            merge_format = 'webm'
        elif format_lower == 'mkv':
            merge_format = 'mkv'
        elif format_lower == 'avi':
            merge_format = 'avi'
        else:  # MP4 default
            merge_format = 'mp4'
        
        output_template = f'{self.output_path}/{next_number:03d}-%(title)s.%(ext)s'
        
        ydl_opts = {
            'format': format_selector,
            'merge_output_format': merge_format,
            'outtmpl': output_template,
            'progress_hooks': [self._progress_hook] if progress_callback else []
        }
        
        # Store callback for progress hook
        if progress_callback:
            self._progress_callback = progress_callback
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            return {'success': True, 'filename': f'Downloaded successfully as {format_choice}'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _progress_hook(self, d):
        """Progress hook for yt-dlp with extensive debugging"""
        try:
            status = d.get('status', 'unknown')
            print(f"Progress hook called with status: {status}")
            
            if hasattr(self, '_progress_callback') and self._progress_callback:
                if d['status'] == 'downloading':
                    # Extract percentage from different possible fields
                    percentage = '0%'
                    if '_percent_str' in d and d['_percent_str']:
                        percentage = d['_percent_str'].strip()
                        print(f"Found _percent_str: {percentage}")
                    elif 'downloaded_bytes' in d and 'total_bytes' in d and d['total_bytes']:
                        pct = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        percentage = f"{pct:.1f}%"
                        print(f"Calculated from bytes: {percentage}")
                    elif 'downloaded_bytes' in d and 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                        pct = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                        percentage = f"{pct:.1f}%"
                        print(f"Calculated from estimate: {percentage}")
                    
                    # Extract speed
                    speed = ''
                    if '_speed_str' in d and d['_speed_str']:
                        speed = d['_speed_str']
                    elif 'speed' in d and d['speed']:
                        speed = f"{d['speed']:.2f}B/s"
                    
                    # Safe filename handling with encoding
                    filename = 'downloading...'
                    try:
                        if 'filename' in d:
                            filename = os.path.basename(d['filename'])
                            # Remove problematic characters
                            filename = filename.encode('ascii', errors='ignore').decode('ascii')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        filename = 'video_file'
                    
                    progress_data = {
                        'status': 'downloading',
                        'percentage': percentage,
                        'speed': speed if speed else 'Unknown',
                        'filename': filename
                    }
                    
                    print(f"Sending progress update: {percentage}")
                    self._progress_callback(progress_data)
                    
                elif d['status'] == 'finished':
                    print("Download finished, sending completion callback")
                    
                    # Safe filename handling
                    filename = 'completed'
                    try:
                        if 'filename' in d:
                            filename = os.path.basename(d['filename'])
                            filename = filename.encode('ascii', errors='ignore').decode('ascii')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        filename = 'video_file'
                    
                    self._progress_callback({
                        'status': 'finished',
                        'filename': filename
                    })
            else:
                print("No progress callback available")
                
        except Exception as e:
            print(f"Error in progress hook: {e}")