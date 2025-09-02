"""
GUI tests for ModernYTDownloader
Testing GUI components with mocking to avoid actual GUI creation
"""
import pytest
import os
import sys
import threading
import time
from unittest.mock import patch, MagicMock, call

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))


class TestModernYTDownloader:
    
    def setup_method(self):
        """Setup test environment"""
        # Mock customtkinter to avoid actual GUI creation
        self.ctk_patcher = patch('customtkinter')
        self.mock_ctk = self.ctk_patcher.start()
        
        # Mock tkinter.filedialog
        self.fd_patcher = patch('tkinter.filedialog')
        self.mock_fd = self.fd_patcher.start()
        
        # Mock VideoDownloader
        self.downloader_patcher = patch('core.downloader.VideoDownloader')
        self.mock_downloader_class = self.downloader_patcher.start()
        self.mock_downloader = MagicMock()
        self.mock_downloader_class.return_value = self.mock_downloader
        
        # Configure mock CTk root window
        self.mock_root = MagicMock()
        self.mock_ctk.CTk.return_value = self.mock_root
        
        # Import after mocking
        from gui.modern_gui import ModernYTDownloader
        self.app = ModernYTDownloader()
    
    def teardown_method(self):
        """Cleanup test environment"""
        self.ctk_patcher.stop()
        self.fd_patcher.stop()
        self.downloader_patcher.stop()
    
    def test_init_gui_setup(self):
        """Test GUI initialization"""
        # Verify CTk configuration calls
        self.mock_ctk.set_appearance_mode.assert_called_once_with("dark")
        self.mock_ctk.set_default_color_theme.assert_called_once_with("blue")
        
        # Verify root window configuration
        self.mock_root.title.assert_called_once_with("YT Downloader Pro")
        self.mock_root.geometry.assert_called_once_with("800x600")
        self.mock_root.minsize.assert_called_once_with(600, 400)
        
        # Verify downloader initialization
        self.mock_downloader_class.assert_called_once()
        assert self.app.downloader == self.mock_downloader
        assert self.app.current_video_info is None
    
    @patch('threading.Thread')
    def test_analyze_video_with_url(self, mock_thread):
        """Test analyze video with valid URL"""
        # Setup mock UI components
        self.app.url_entry = MagicMock()
        self.app.url_entry.get.return_value = "https://youtube.com/watch?v=test"
        self.app.analyze_btn = MagicMock()
        self.app.download_btn = MagicMock()
        
        self.app.analyze_video()
        
        # Verify UI state changes
        self.app.analyze_btn.configure.assert_called_with(state="disabled", text="Analyzing...")
        self.app.download_btn.configure.assert_called_with(state="disabled")
        
        # Verify thread creation
        mock_thread.assert_called_once()
        thread_args = mock_thread.call_args[1]
        assert thread_args['target'] == self.app._analyze_video_thread
        assert thread_args['args'] == ("https://youtube.com/watch?v=test",)
    
    @patch('gui.modern_gui.ModernYTDownloader.show_status')
    def test_analyze_video_no_url(self, mock_show_status):
        """Test analyze video with empty URL"""
        self.app.url_entry = MagicMock()
        self.app.url_entry.get.return_value = ""
        
        self.app.analyze_video()
        
        mock_show_status.assert_called_once_with("Please enter a URL", "error")
    
    def test_analyze_video_thread_success(self):
        """Test video analysis thread with successful result"""
        # Mock video info
        mock_info = {
            'title': 'Test Video',
            'duration': 180,
            'formats': [
                {'quality': '1080p', 'format_id': 'test1080'},
                {'quality': '720p', 'format_id': 'test720'}
            ]
        }
        self.mock_downloader.get_video_info.return_value = mock_info
        
        # Mock root.after to simulate main thread callback
        self.app.root = MagicMock()
        
        self.app._analyze_video_thread("https://youtube.com/watch?v=test")
        
        # Verify downloader was called
        self.mock_downloader.get_video_info.assert_called_once_with("https://youtube.com/watch?v=test")
        
        # Verify main thread callback was scheduled
        self.app.root.after.assert_called_once()
        call_args = self.app.root.after.call_args[0]
        assert call_args[0] == 0  # Immediate callback
        assert call_args[1] == self.app._update_video_info
    
    def test_analyze_video_thread_error(self):
        """Test video analysis thread with error"""
        self.mock_downloader.get_video_info.side_effect = Exception("Network error")
        self.app.root = MagicMock()
        
        self.app._analyze_video_thread("https://youtube.com/watch?v=test")
        
        # Verify error callback was scheduled
        self.app.root.after.assert_called_once()
        call_args = self.app.root.after.call_args[0]
        assert call_args[1] == self.app._show_analysis_error
        assert call_args[2] == "Network error"
    
    def test_update_video_info_success(self):
        """Test successful video info update"""
        # Setup mock UI components
        self.app.analyze_btn = MagicMock()
        self.app.info_text = MagicMock()
        self.app.quality_menu = MagicMock()
        self.app.quality_var = MagicMock()
        self.app.download_btn = MagicMock()
        
        mock_info = {
            'title': 'Test Video',
            'duration': 180,
            'formats': [
                {'quality': '1080p'}, 
                {'quality': '720p'}
            ]
        }
        
        self.app._update_video_info(mock_info, "https://youtube.com/watch?v=test")
        
        # Verify UI updates
        self.app.analyze_btn.configure.assert_called_with(state="normal", text="Analyze")
        self.app.info_text.delete.assert_called()
        self.app.info_text.insert.assert_called()
        self.app.quality_menu.configure.assert_called_with(values=['1080p', '720p'])
        self.app.download_btn.configure.assert_called_with(state="normal")
        
        # Verify info storage
        assert self.app.current_video_info == mock_info
    
    def test_update_video_info_error(self):
        """Test video info update with error"""
        self.app.analyze_btn = MagicMock()
        self.app.info_text = MagicMock()
        
        error_info = {'error': 'Video not found'}
        
        self.app._update_video_info(error_info, "https://youtube.com/watch?v=test")
        
        # Verify error display
        self.app.analyze_btn.configure.assert_called_with(state="normal", text="Analyze")
        insert_call = self.app.info_text.insert.call_args[0]
        assert "Error: Video not found" in insert_call[1]
    
    @patch('threading.Thread')
    def test_start_download_with_url(self, mock_thread):
        """Test start download with valid URL"""
        # Setup mock UI components
        self.app.url_entry = MagicMock()
        self.app.url_entry.get.return_value = "https://youtube.com/watch?v=test"
        self.app.quality_var = MagicMock()
        self.app.quality_var.get.return_value = "720p"
        self.app.folder_entry = MagicMock()
        self.app.folder_entry.get.return_value = "/test/path"
        self.app.download_btn = MagicMock()
        self.app.progress_bar = MagicMock()
        
        self.app.start_download()
        
        # Verify UI state changes
        self.app.download_btn.configure.assert_called_with(state="disabled", text="Downloading...")
        self.app.progress_bar.set.assert_called_with(0)
        
        # Verify thread creation
        mock_thread.assert_called_once()
        thread_args = mock_thread.call_args[1]
        assert thread_args['target'] == self.app._download_thread
    
    @patch('gui.modern_gui.ModernYTDownloader.show_status')
    def test_start_download_no_url(self, mock_show_status):
        """Test start download with empty URL"""
        self.app.url_entry = MagicMock()
        self.app.url_entry.get.return_value = ""
        
        self.app.start_download()
        
        mock_show_status.assert_called_once_with("Please enter a URL", "error")
    
    def test_download_thread_success(self):
        """Test download thread with successful result"""
        mock_result = {'success': True, 'filename': 'test.mp4'}
        self.mock_downloader.download_video.return_value = mock_result
        self.app.root = MagicMock()
        
        self.app._download_thread("https://youtube.com/watch?v=test", "720p")
        
        # Verify downloader was called with progress callback
        self.mock_downloader.download_video.assert_called_once_with(
            "https://youtube.com/watch?v=test", 
            "720p", 
            progress_callback=self.app._progress_callback
        )
        
        # Verify success callback was scheduled
        self.app.root.after.assert_called_once()
        call_args = self.app.root.after.call_args[0]
        assert call_args[1] == self.app._download_finished
        assert call_args[2] == mock_result
    
    def test_download_thread_error(self):
        """Test download thread with error"""
        self.mock_downloader.download_video.side_effect = Exception("Download failed")
        self.app.root = MagicMock()
        
        self.app._download_thread("https://youtube.com/watch?v=test", "720p")
        
        # Verify error callback was scheduled
        self.app.root.after.assert_called_once()
        call_args = self.app.root.after.call_args[0]
        assert call_args[1] == self.app._download_error
        assert call_args[2] == "Download failed"
    
    def test_progress_callback(self):
        """Test progress callback scheduling"""
        self.app.root = MagicMock()
        progress_info = {'status': 'downloading', 'percentage': '50%'}
        
        self.app._progress_callback(progress_info)
        
        # Verify progress update was scheduled
        self.app.root.after.assert_called_once_with(0, self.app._update_progress, progress_info)
    
    def test_update_progress_downloading(self):
        """Test progress update during download"""
        self.app.progress_bar = MagicMock()
        self.app.status_label = MagicMock()
        
        progress_info = {
            'status': 'downloading',
            'percentage': '75%',
            'speed': '2.5MiB/s',
            'filename': 'test.mp4'
        }
        
        self.app._update_progress(progress_info)
        
        # Verify progress bar update
        self.app.progress_bar.set.assert_called_with(0.75)
        
        # Verify status label update
        expected_text = "Downloading: test.mp4 - 2.5MiB/s"
        self.app.status_label.configure.assert_called_with(text=expected_text)
    
    def test_update_progress_finished(self):
        """Test progress update when finished"""
        self.app.progress_bar = MagicMock()
        self.app.status_label = MagicMock()
        
        progress_info = {
            'status': 'finished',
            'filename': 'test.mp4'
        }
        
        self.app._update_progress(progress_info)
        
        # Verify progress bar completion
        self.app.progress_bar.set.assert_called_with(1.0)
        
        # Verify status label update
        self.app.status_label.configure.assert_called_with(text="Completed: test.mp4")
    
    @patch('gui.modern_gui.ModernYTDownloader.show_status')
    def test_download_finished_success(self, mock_show_status):
        """Test download finished with success"""
        self.app.download_btn = MagicMock()
        self.app.progress_bar = MagicMock()
        
        result = {'success': True}
        self.app._download_finished(result)
        
        # Verify UI reset
        self.app.download_btn.configure.assert_called_with(state="normal", text="📥 Download")
        self.app.progress_bar.set.assert_called_with(1.0)
        mock_show_status.assert_called_with("Download completed successfully!", "success")
    
    @patch('gui.modern_gui.ModernYTDownloader.show_status')
    def test_download_finished_error(self, mock_show_status):
        """Test download finished with error"""
        self.app.download_btn = MagicMock()
        self.app.progress_bar = MagicMock()
        
        result = {'success': False, 'error': 'Network timeout'}
        self.app._download_finished(result)
        
        # Verify UI reset and error display
        self.app.download_btn.configure.assert_called_with(state="normal", text="📥 Download")
        self.app.progress_bar.set.assert_called_with(0)
        mock_show_status.assert_called_with("Download failed: Network timeout", "error")
    
    def test_browse_folder(self):
        """Test folder browsing functionality"""
        self.mock_fd.askdirectory.return_value = "/new/folder"
        self.app.folder_entry = MagicMock()
        self.app.folder_entry.get.return_value = "/old/folder"
        
        self.app.browse_folder()
        
        # Verify folder selection
        self.mock_fd.askdirectory.assert_called_once_with(initialdir=self.mock_downloader.output_path)
        
        # Verify UI update
        self.app.folder_entry.delete.assert_called_with(0, self.mock_ctk.END)
        self.app.folder_entry.insert.assert_called_with(0, "/new/folder")
        
        # Verify downloader path update
        assert self.mock_downloader.output_path == "/new/folder"
    
    def test_format_duration_hours(self):
        """Test duration formatting with hours"""
        result = self.app._format_duration(3661)  # 1:01:01
        assert result == "01:01:01"
    
    def test_format_duration_minutes(self):
        """Test duration formatting without hours"""
        result = self.app._format_duration(125)  # 2:05
        assert result == "02:05"
    
    def test_format_duration_zero(self):
        """Test duration formatting with zero"""
        result = self.app._format_duration(0)
        assert result == "Unknown"
    
    def test_show_status(self):
        """Test status display"""
        self.app.status_label = MagicMock()
        
        self.app.show_status("Test message", "info")
        
        self.app.status_label.configure.assert_called_with(text="Test message")


if __name__ == '__main__':
    pytest.main([__file__])