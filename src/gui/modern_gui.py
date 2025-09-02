"""
Modern GUI for YouTube Downloader using CustomTkinter
Features: Dark theme, quality selection, progress tracking
"""
import customtkinter as ctk
import threading
import tkinter.filedialog as fd
from PIL import Image
import requests
from io import BytesIO
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.downloader import VideoDownloader


class ModernYTDownloader:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("YT Downloader Pro")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Initialize downloader
        self.downloader = VideoDownloader()
        self.current_video_info = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="🎥 YouTube Downloader Pro", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(20, 30))
        
        # URL input section
        self.setup_url_section()
        
        # Video info section
        self.setup_video_info_section()
        
        # Download options section
        self.setup_download_options()
        
        # Progress section
        self.setup_progress_section()
        
        # Output folder section
        self.setup_folder_section()
        
    def setup_url_section(self):
        """Setup URL input section"""
        url_frame = ctk.CTkFrame(self.main_frame)
        url_frame.pack(fill="x", pady=(0, 20))
        
        url_label = ctk.CTkLabel(url_frame, text="Video URL:", font=ctk.CTkFont(size=14, weight="bold"))
        url_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        url_input_frame = ctk.CTkFrame(url_frame)
        url_input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.url_entry = ctk.CTkEntry(
            url_input_frame,
            placeholder_text="Paste YouTube URL or m3u8 stream here...",
            font=ctk.CTkFont(size=12)
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        self.analyze_btn = ctk.CTkButton(
            url_input_frame,
            text="Analyze",
            command=self.analyze_video,
            width=100
        )
        self.analyze_btn.pack(side="right", padx=(5, 10), pady=10)
        
    def setup_video_info_section(self):
        """Setup video information display"""
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(fill="x", pady=(0, 20))
        
        info_label = ctk.CTkLabel(self.info_frame, text="Video Information:", font=ctk.CTkFont(size=14, weight="bold"))
        info_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Info display area
        self.info_text = ctk.CTkTextbox(self.info_frame, height=100)
        self.info_text.pack(fill="x", padx=20, pady=(0, 20))
        self.info_text.insert("0.0", "Enter a URL and click 'Analyze' to see video information...")
        
    def setup_download_options(self):
        """Setup download options"""
        options_frame = ctk.CTkFrame(self.main_frame)
        options_frame.pack(fill="x", pady=(0, 20))
        
        options_label = ctk.CTkLabel(options_frame, text="Download Options:", font=ctk.CTkFont(size=14, weight="bold"))
        options_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Quality selection
        quality_frame = ctk.CTkFrame(options_frame)
        quality_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(quality_frame, text="Quality:", font=ctk.CTkFont(size=12)).pack(side="left", padx=10, pady=10)
        
        self.quality_var = ctk.StringVar(value="best")
        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            variable=self.quality_var,
            values=["best", "1080p", "720p", "480p", "360p", "bestaudio"]
        )
        self.quality_menu.pack(side="left", padx=10, pady=10)
        
        # Download button
        self.download_btn = ctk.CTkButton(
            options_frame,
            text="📥 Download",
            command=self.start_download,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            state="disabled"
        )
        self.download_btn.pack(pady=20)
        
    def setup_progress_section(self):
        """Setup progress tracking"""
        progress_frame = ctk.CTkFrame(self.main_frame)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        progress_label = ctk.CTkLabel(progress_frame, text="Download Progress:", font=ctk.CTkFont(size=14, weight="bold"))
        progress_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(progress_frame, text="Ready to download")
        self.status_label.pack(padx=20, pady=(0, 20))
        
    def setup_folder_section(self):
        """Setup output folder selection"""
        folder_frame = ctk.CTkFrame(self.main_frame)
        folder_frame.pack(fill="x")
        
        folder_label = ctk.CTkLabel(folder_frame, text="Output Folder:", font=ctk.CTkFont(size=14, weight="bold"))
        folder_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        folder_input_frame = ctk.CTkFrame(folder_frame)
        folder_input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.folder_entry = ctk.CTkEntry(
            folder_input_frame,
            placeholder_text="Output folder path...",
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        self.folder_entry.insert(0, self.downloader.output_path)
        
        browse_btn = ctk.CTkButton(
            folder_input_frame,
            text="Browse",
            command=self.browse_folder,
            width=100
        )
        browse_btn.pack(side="right", padx=(5, 10), pady=10)
        
    def browse_folder(self):
        """Browse for output folder"""
        folder = fd.askdirectory(initialdir=self.downloader.output_path)
        if folder:
            self.folder_entry.delete(0, ctk.END)
            self.folder_entry.insert(0, folder)
            self.downloader.output_path = folder
            
    def analyze_video(self):
        """Analyze video URL in separate thread"""
        url = self.url_entry.get().strip()
        if not url:
            self.show_status("Please enter a URL", "error")
            return
            
        self.analyze_btn.configure(state="disabled", text="Analyzing...")
        self.download_btn.configure(state="disabled")
        
        # Run analysis in thread to prevent GUI freezing
        thread = threading.Thread(target=self._analyze_video_thread, args=(url,))
        thread.daemon = True
        thread.start()
        
    def _analyze_video_thread(self, url):
        """Thread function for video analysis"""
        try:
            info = self.downloader.get_video_info(url)
            
            # Update GUI in main thread
            self.root.after(0, self._update_video_info, info, url)
            
        except Exception as e:
            self.root.after(0, self._show_analysis_error, str(e))
            
    def _update_video_info(self, info, url):
        """Update video information display"""
        self.analyze_btn.configure(state="normal", text="Analyze")
        
        if 'error' in info:
            self.info_text.delete("0.0", ctk.END)
            self.info_text.insert("0.0", f"Error: {info['error']}")
            return
            
        # Store info and update display
        self.current_video_info = info
        
        info_text = f"Title: {info.get('title', 'Unknown')}\\n"
        info_text += f"Duration: {self._format_duration(info.get('duration', 0))}\\n"
        
        if 'formats' in info and info['formats']:
            info_text += f"Available qualities: {', '.join([f['quality'] for f in info['formats']])}"
            
            # Update quality menu
            qualities = [f['quality'] for f in info['formats']]
            self.quality_menu.configure(values=qualities)
            if qualities:
                self.quality_var.set(qualities[0])
        
        self.info_text.delete("0.0", ctk.END)
        self.info_text.insert("0.0", info_text)
        
        # Enable download button
        self.download_btn.configure(state="normal")
        
    def _show_analysis_error(self, error):
        """Show analysis error"""
        self.analyze_btn.configure(state="normal", text="Analyze")
        self.info_text.delete("0.0", ctk.END)
        self.info_text.insert("0.0", f"Analysis failed: {error}")
        
    def start_download(self):
        """Start download in separate thread"""
        url = self.url_entry.get().strip()
        quality = self.quality_var.get()
        
        if not url:
            self.show_status("Please enter a URL", "error")
            return
            
        # Update folder path
        self.downloader.output_path = self.folder_entry.get()
        
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.progress_bar.set(0)
        
        # Start download thread
        thread = threading.Thread(target=self._download_thread, args=(url, quality))
        thread.daemon = True
        thread.start()
        
    def _download_thread(self, url, quality):
        """Thread function for downloading"""
        try:
            result = self.downloader.download_video(
                url, 
                quality, 
                progress_callback=self._progress_callback
            )
            
            self.root.after(0, self._download_finished, result)
            
        except Exception as e:
            self.root.after(0, self._download_error, str(e))
            
    def _progress_callback(self, progress_info):
        """Handle progress updates"""
        self.root.after(0, self._update_progress, progress_info)
        
    def _update_progress(self, progress_info):
        """Update progress display"""
        status = progress_info.get('status', '')
        
        if status == 'downloading':
            percentage = progress_info.get('percentage', '0%').replace('%', '')
            try:
                self.progress_bar.set(float(percentage) / 100)
            except ValueError:
                pass
            
            speed = progress_info.get('speed', '')
            filename = progress_info.get('filename', '')
            self.status_label.configure(text=f"Downloading: {filename} - {speed}")
            
        elif status == 'finished':
            self.progress_bar.set(1.0)
            filename = progress_info.get('filename', '')
            self.status_label.configure(text=f"Completed: {filename}")
            
    def _download_finished(self, result):
        """Handle download completion"""
        self.download_btn.configure(state="normal", text="📥 Download")
        
        if result.get('success'):
            self.show_status("Download completed successfully!", "success")
            self.progress_bar.set(1.0)
        else:
            self.show_status(f"Download failed: {result.get('error', 'Unknown error')}", "error")
            self.progress_bar.set(0)
            
    def _download_error(self, error):
        """Handle download error"""
        self.download_btn.configure(state="normal", text="📥 Download")
        self.show_status(f"Download error: {error}", "error")
        self.progress_bar.set(0)
        
    def show_status(self, message, status_type="info"):
        """Show status message"""
        self.status_label.configure(text=message)
        
        # You could add different colors based on status_type if needed
        
    def _format_duration(self, seconds):
        """Format duration in seconds to readable format"""
        if not seconds:
            return "Unknown"
            
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
            
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    app = ModernYTDownloader()
    app.run()


if __name__ == "__main__":
    main()