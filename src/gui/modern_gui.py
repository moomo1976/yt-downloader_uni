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
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        
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
        
        # Download button - make it more prominent
        download_container = ctk.CTkFrame(options_frame)
        download_container.pack(fill="x", padx=20, pady=20)
        
        self.download_btn = ctk.CTkButton(
            download_container,
            text="📥 DOWNLOAD VIDEO",
            command=self.start_download,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            state="normal",
            fg_color=("#1f538d", "#14375e"),
            hover_color=("#14375e", "#1f538d")
        )
        self.download_btn.pack(pady=15, padx=20, fill="x")
        
    def setup_progress_section(self):
        """Setup progress tracking with better visualization"""
        progress_frame = ctk.CTkFrame(self.main_frame)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        progress_label = ctk.CTkLabel(progress_frame, text="📊 Download Progress:", font=ctk.CTkFont(size=14, weight="bold"))
        progress_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Progress bar with percentage
        progress_container = ctk.CTkFrame(progress_frame)
        progress_container.pack(fill="x", padx=20, pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_container, height=20)
        self.progress_bar.pack(fill="x", padx=10, pady=10)
        self.progress_bar.set(0)
        
        # Progress percentage label
        self.progress_percentage = ctk.CTkLabel(progress_container, text="0%", font=ctk.CTkFont(size=12, weight="bold"))
        self.progress_percentage.pack(pady=5)
        
        # Status with icons
        self.status_label = ctk.CTkLabel(progress_frame, text="⏳ Ready to download", font=ctk.CTkFont(size=12))
        self.status_label.pack(padx=20, pady=5)
        
        # Download speed
        self.speed_label = ctk.CTkLabel(progress_frame, text="Speed: --", font=ctk.CTkFont(size=11))
        self.speed_label.pack(padx=20, pady=5)
        
        # File info
        self.file_info_label = ctk.CTkLabel(progress_frame, text="File: Not selected", font=ctk.CTkFont(size=11))
        self.file_info_label.pack(padx=20, pady=(5, 20))
        
    def setup_folder_section(self):
        """Setup output folder selection with better visibility"""
        folder_frame = ctk.CTkFrame(self.main_frame)
        folder_frame.pack(fill="x", pady=(0, 20))
        
        folder_label = ctk.CTkLabel(folder_frame, text="📁 Download Destination:", font=ctk.CTkFont(size=14, weight="bold"))
        folder_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Current folder display
        current_folder_frame = ctk.CTkFrame(folder_frame)
        current_folder_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        ctk.CTkLabel(current_folder_frame, text="Current folder:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.current_folder_label = ctk.CTkLabel(
            current_folder_frame, 
            text=self.downloader.output_path, 
            font=ctk.CTkFont(size=11),
            text_color=("#1f538d", "#14375e")
        )
        self.current_folder_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Folder selection buttons
        folder_buttons_frame = ctk.CTkFrame(folder_frame)
        folder_buttons_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        browse_btn = ctk.CTkButton(
            folder_buttons_frame,
            text="📁 Choose Download Folder",
            command=self.browse_folder,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=("#2d8659", "#1e5a3a"),
            hover_color=("#1e5a3a", "#2d8659")
        )
        browse_btn.pack(fill="x", padx=10, pady=10)
        
        # Open folder button
        self.open_folder_btn = ctk.CTkButton(
            folder_buttons_frame,
            text="📂 Open Downloads Folder",
            command=self.open_downloads_folder,
            font=ctk.CTkFont(size=12),
            height=35,
            fg_color=("gray60", "gray40"),
            hover_color=("gray50", "gray30")
        )
        self.open_folder_btn.pack(fill="x", padx=10, pady=(0, 20))
        
    def browse_folder(self):
        """Browse for output folder"""
        folder = fd.askdirectory(initialdir=self.downloader.output_path, title="Choose Download Folder")
        if folder:
            self.downloader.output_path = folder
            self.current_folder_label.configure(text=folder)
            self.show_status(f"✅ Download folder set to: {folder}", "success")
    
    def open_downloads_folder(self):
        """Open downloads folder in file explorer"""
        import os
        import subprocess
        import platform
        
        try:
            if platform.system() == "Windows":
                os.startfile(self.downloader.output_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", self.downloader.output_path])
            else:  # Linux
                subprocess.run(["xdg-open", self.downloader.output_path])
            self.show_status("📂 Opened downloads folder", "success")
        except Exception as e:
            self.show_status(f"❌ Could not open folder: {str(e)}", "error")
            
    def analyze_video(self):
        """Analyze video URL in separate thread"""
        url = self.url_entry.get().strip()
        if not url:
            self.show_status("Please enter a URL", "error")
            return
            
        self.analyze_btn.configure(state="disabled", text="Analyzing...")
        
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
            
        self.download_btn.configure(state="disabled", text="DOWNLOADING...")
        self.progress_bar.set(0)
        self.progress_percentage.configure(text="0%")
        self.status_label.configure(text="🚀 Starting download...")
        self.speed_label.configure(text="Speed: --")
        self.file_info_label.configure(text="File: Preparing...")
        
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
        """Update progress display with enhanced visualization"""
        status = progress_info.get('status', '')
        
        if status == 'downloading':
            percentage_str = progress_info.get('percentage', '0%')
            percentage = percentage_str.replace('%', '')
            
            try:
                progress_val = float(percentage) / 100
                self.progress_bar.set(progress_val)
                self.progress_percentage.configure(text=percentage_str)
            except ValueError:
                pass
            
            speed = progress_info.get('speed', '')
            filename = progress_info.get('filename', '')
            
            # Update all progress elements
            self.status_label.configure(text=f"⬇️ Downloading: {filename}")
            self.speed_label.configure(text=f"Speed: {speed}")
            self.file_info_label.configure(text=f"File: {filename}")
            
        elif status == 'finished':
            self.progress_bar.set(1.0)
            self.progress_percentage.configure(text="100%")
            filename = progress_info.get('filename', '')
            
            # Update status to completed
            self.status_label.configure(text=f"✅ Completed: {filename}")
            self.speed_label.configure(text="Speed: Download finished")
            self.file_info_label.configure(text=f"📁 Saved to: {self.downloader.output_path}")
            
    def _download_finished(self, result):
        """Handle download completion"""
        self.download_btn.configure(state="normal", text="📥 DOWNLOAD VIDEO")
        
        if result.get('success'):
            self.show_status("Download completed successfully!", "success")
            self.progress_bar.set(1.0)
        else:
            self.show_status(f"Download failed: {result.get('error', 'Unknown error')}", "error")
            self.progress_bar.set(0)
            
    def _download_error(self, error):
        """Handle download error"""
        self.download_btn.configure(state="normal", text="📥 DOWNLOAD VIDEO")
        self.show_status(f"Download error: {error}", "error")
        self.progress_bar.set(0)
        
    def show_status(self, message, status_type="info"):
        """Show status message with visual feedback"""
        # Update main status label
        if hasattr(self, 'status_label'):
            if status_type == "error":
                self.status_label.configure(text=f"❌ {message}")
            elif status_type == "success":
                self.status_label.configure(text=f"✅ {message}")
            else:
                self.status_label.configure(text=f"ℹ️ {message}")
        
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