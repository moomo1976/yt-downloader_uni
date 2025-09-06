#!/usr/bin/env python3
"""
Simple and Clear GUI for YouTube Downloader
Focused on visibility and functionality
"""
import customtkinter as ctk
import threading
import tkinter.filedialog as fd
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.downloader import VideoDownloader
from core.dependency_checker import DependencyChecker
from version import APP_TITLE


class SimpleYTDownloader:
    def __init__(self):
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize main window
        self.root = ctk.CTk()
        try:
            self.root.title(f"🎥 {APP_TITLE}")
        except UnicodeEncodeError:
            self.root.title(APP_TITLE)
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # Check dependencies before proceeding
        self.dependency_checker = DependencyChecker()
        dependency_results = self.dependency_checker.check_all_dependencies()
        
        # Initialize downloader
        self.downloader = VideoDownloader()
        
        self.setup_ui()
        self.setup_menu()
        
        # Show dependency warning if needed
        if not dependency_results['all_ok']:
            self.show_dependency_warning(dependency_results)
        
    def setup_ui(self):
        """Setup simple and clear UI"""
        # Main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        try:
            title_text = f"🎥 {APP_TITLE}"
        except:
            title_text = APP_TITLE
        title = ctk.CTkLabel(
            self.main_frame,
            text=title_text,
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        # URL Input Section
        self.create_url_section()
        
        # Folder Selection Section  
        self.create_folder_section()
        
        # Quality Selection Section
        self.create_quality_section()
        
        # Download Button
        self.create_download_button()
        
        # Progress Section
        self.create_progress_section()
        
    def create_url_section(self):
        """Create URL input section"""
        # URL Frame
        url_frame = ctk.CTkFrame(self.main_frame)
        url_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            url_frame,
            text="📎 Video URL:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # URL Input
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Paste YouTube URL here (e.g., https://youtube.com/watch?v=...)",
            font=ctk.CTkFont(size=12),
            height=40
        )
        self.url_entry.pack(fill="x", padx=20, pady=(0, 20))
        
    def create_folder_section(self):
        """Create folder selection section"""
        folder_frame = ctk.CTkFrame(self.main_frame)
        folder_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            folder_frame,
            text="📁 Download Location:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Current folder display
        self.current_folder_label = ctk.CTkLabel(
            folder_frame,
            text=f"Current: {self.downloader.output_path}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.current_folder_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Folder buttons
        button_frame = ctk.CTkFrame(folder_frame)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Choose folder button
        choose_btn = ctk.CTkButton(
            button_frame,
            text="📁 Choose Download Folder",
            command=self.browse_folder,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            fg_color="#28a745",
            hover_color="#218838"
        )
        choose_btn.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        # Open folder button
        open_btn = ctk.CTkButton(
            button_frame,
            text="📂 Open Folder",
            command=self.open_folder,
            font=ctk.CTkFont(size=14),
            height=45,
            fg_color="gray60",
            hover_color="gray50"
        )
        open_btn.pack(side="right", fill="x", expand=True, padx=(5, 10), pady=10)
        
    def create_quality_section(self):
        """Create quality and format selection section"""
        quality_frame = ctk.CTkFrame(self.main_frame)
        quality_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            quality_frame,
            text="🎯 Download Options:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Options container
        options_container = ctk.CTkFrame(quality_frame)
        options_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Quality selection
        ctk.CTkLabel(
            options_container,
            text="Quality:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.quality_var = ctk.StringVar(value="720p")
        self.quality_menu = ctk.CTkOptionMenu(
            options_container,
            variable=self.quality_var,
            values=["Best Quality", "1080p", "720p", "480p", "360p", "Audio Only"],
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.quality_menu.pack(fill="x", padx=20, pady=(0, 10))
        
        # Format selection
        ctk.CTkLabel(
            options_container,
            text="Format:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.format_var = ctk.StringVar(value="MP4")
        self.format_menu = ctk.CTkOptionMenu(
            options_container,
            variable=self.format_var,
            values=["MP4", "MP3", "WEBM", "AVI"],
            font=ctk.CTkFont(size=13),
            height=35
        )
        self.format_menu.pack(fill="x", padx=20, pady=(0, 20))
        
    def create_download_button(self):
        """Create prominent download button"""
        self.download_btn = ctk.CTkButton(
            self.main_frame,
            text="⬇️ DOWNLOAD VIDEO",
            command=self.start_download,
            font=ctk.CTkFont(size=18, weight="bold"),
            height=60,
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        self.download_btn.pack(fill="x", pady=20)
        
    def create_progress_section(self):
        """Create progress display section"""
        progress_frame = ctk.CTkFrame(self.main_frame)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            progress_frame,
            text="📊 Download Progress:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=25
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Progress percentage
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.progress_label.pack(pady=5)
        
        # Status display
        self.status_label = ctk.CTkLabel(
            progress_frame,
            text="⏳ Ready to download",
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(pady=5)
        
        # Speed and file info
        self.info_label = ctk.CTkLabel(
            progress_frame,
            text="Select a video to download",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.info_label.pack(pady=(5, 20))
    
    def setup_menu(self):
        """Setup application menu bar"""
        import tkinter as tk
        
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.configure(menu=menubar)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Nástroje", menu=tools_menu)
        tools_menu.add_command(label="🔍 Kontrola závislostí", command=self.check_dependencies_menu)
        tools_menu.add_separator()
        tools_menu.add_command(label="📂 Otevřít složku stažených", command=self.open_folder)
        
    def browse_folder(self):
        """Browse for download folder"""
        folder = fd.askdirectory(
            initialdir=self.downloader.output_path,
            title="Choose Download Folder"
        )
        if folder:
            self.downloader.output_path = folder
            self.current_folder_label.configure(text=f"Current: {folder}")
            self.status_label.configure(text=f"✅ Folder set: {os.path.basename(folder)}")
            
    def open_folder(self):
        """Open download folder"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.downloader.output_path)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{self.downloader.output_path}"')
            self.status_label.configure(text="📂 Opened download folder")
        except Exception as e:
            self.status_label.configure(text=f"❌ Error opening folder: {str(e)}")
            
    def start_download(self):
        """Start video download"""
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="❌ Please enter a video URL")
            return
            
        # Get quality and format
        quality = self.quality_var.get()
        format_choice = self.format_var.get()
        
        # Process quality
        if quality == "Best Quality":
            quality = "best"
        elif quality == "Audio Only":
            quality = "bestaudio"
        else:
            quality = quality.lower()  # "1080p" -> "1080p"
            
        # Update UI
        self.download_btn.configure(state="disabled", text="⬇️ DOWNLOADING...")
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.status_label.configure(text="🚀 Starting download...")
        self.info_label.configure(text=f"Format: {format_choice} | Quality: {quality}")
        
        # Start download in thread
        thread = threading.Thread(
            target=self._download_thread,
            args=(url, quality, format_choice),
            daemon=True
        )
        thread.start()
        
    def _download_thread(self, url, quality, format_choice):
        """Download thread"""
        try:
            result = self.downloader.download_video_with_format(
                url,
                quality,
                format_choice,
                progress_callback=self._progress_callback
            )
            
            # Update UI on main thread
            self.root.after(0, self._download_finished, result)
            
        except Exception as e:
            self.root.after(0, self._download_error, str(e))
            
    def _progress_callback(self, progress_info):
        """Handle progress updates"""
        print(f"GUI received progress callback: {progress_info}")
        self.root.after(0, self._update_progress, progress_info)
        
    def _update_progress(self, progress_info):
        """Update progress display"""
        print(f"GUI updating progress with: {progress_info}")
        status = progress_info.get('status', '')
        
        if status == 'downloading':
            # Update progress bar and percentage
            percentage_str = progress_info.get('percentage', '0%')
            print(f"Processing percentage string: '{percentage_str}'")
            
            try:
                # Remove % and any extra characters
                percentage_clean = percentage_str.replace('%', '').strip()
                percentage = float(percentage_clean)
                
                # Update progress bar (0-1 scale)
                progress_value = min(max(percentage / 100, 0), 1)  # Clamp between 0-1
                self.progress_bar.set(progress_value)
                self.progress_label.configure(text=f"{percentage:.1f}%")
                
                print(f"Progress bar updated to: {percentage:.1f}% (value: {progress_value})")
                
            except (ValueError, TypeError) as e:
                print(f"Error parsing percentage '{percentage_str}': {e}")
                # Set some progress anyway
                self.progress_label.configure(text="Downloading...")
                
            # Update status and info
            speed = progress_info.get('speed', 'Unknown')
            filename = progress_info.get('filename', 'downloading...')
            
            self.status_label.configure(text=f"⬇️ Downloading: {os.path.basename(filename)}")
            self.info_label.configure(text=f"Speed: {speed} | File: {os.path.basename(filename)}")
            
        elif status == 'finished':
            print("Setting progress to 100%")
            self.progress_bar.set(1.0)
            self.progress_label.configure(text="100%")
            filename = progress_info.get('filename', '')
            self.status_label.configure(text=f"✅ Download completed!")
            self.info_label.configure(text=f"Saved: {os.path.basename(filename)}")
            print("Download finished - GUI updated!")
            
    def _download_finished(self, result):
        """Handle download completion"""
        self.download_btn.configure(state="normal", text="⬇️ DOWNLOAD VIDEO")
        
        if result.get('success'):
            self.progress_bar.set(1.0)
            self.progress_label.configure(text="100%")
            self.status_label.configure(text="🎉 Download completed successfully!")
            self.info_label.configure(text=f"Saved to: {self.downloader.output_path}")
        else:
            self.progress_bar.set(0)
            self.progress_label.configure(text="0%")
            error_msg = result.get('error', 'Unknown error')
            self.status_label.configure(text=f"❌ Download failed: {error_msg}")
            self.info_label.configure(text="Please try again")
            
    def _download_error(self, error):
        """Handle download error"""
        self.download_btn.configure(state="normal", text="⬇️ DOWNLOAD VIDEO")
        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.status_label.configure(text=f"❌ Error: {error}")
        self.info_label.configure(text="Please check the URL and try again")
    
    def show_dependency_warning(self, dependency_results):
        """Show warning dialog for missing dependencies"""
        import tkinter.messagebox as msgbox
        
        missing_deps = []
        
        # Collect missing system dependencies
        for dep_name, info in dependency_results['system'].items():
            if not info['available'] and info['required']:
                missing_deps.append(f"• {info['description']}")
        
        # Collect missing Python dependencies
        python_missing = []
        for module_name, info in dependency_results['python'].items():
            if not info['available'] and info['required']:
                missing_deps.append(f"• {info['description']}")
                python_missing.append(info['package'])
        
        if missing_deps:
            warning_msg = "⚠️ CHYBĚJÍCÍ KOMPONENTY:\n\n"
            warning_msg += "\n".join(missing_deps)
            
            if python_missing:
                warning_msg += f"\n\n💡 Instalace Python balíčků:\n"
                warning_msg += f"pip install {' '.join(python_missing)}"
            
            warning_msg += "\n\n⚠️ Bez těchto komponent nemusí aplikace fungovat správně!"
            
            # Show warning dialog
            result = msgbox.showwarning(
                "Chybějící komponenty",
                warning_msg
            )
    
    def check_dependencies_menu(self):
        """Check dependencies and show detailed report"""
        import tkinter.messagebox as msgbox
        
        results = self.dependency_checker.check_all_dependencies()
        
        if results['all_ok']:
            msgbox.showinfo(
                "Kontrola závislostí",
                "✅ Všechny požadované komponenty jsou dostupné!\n\nAplikace je připravena k použití."
            )
        else:
            report = self.dependency_checker.get_missing_dependencies_report()
            msgbox.showerror(
                "Chybějící komponenty",
                report
            )
        
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    app = SimpleYTDownloader()
    app.run()


if __name__ == "__main__":
    main()