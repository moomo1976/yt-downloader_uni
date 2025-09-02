"""
Unit tests for VideoDownloader core functionality
"""
import pytest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock, call
import sys

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from core.downloader import VideoDownloader


class TestVideoDownloader:
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.downloader = VideoDownloader(output_path=self.temp_dir)
    
    def teardown_method(self):
        """Cleanup test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_init_default_path(self):
        """Test VideoDownloader initialization with default path"""
        downloader = VideoDownloader()
        expected_path = os.path.join(os.path.expanduser("~"), "Downloads", "YT_Downloads")
        assert downloader.output_path == expected_path
    
    def test_init_custom_path(self):
        """Test VideoDownloader initialization with custom path"""
        custom_path = "/custom/path"
        downloader = VideoDownloader(output_path=custom_path)
        assert downloader.output_path == custom_path
    
    def test_ensure_output_dir(self):
        """Test output directory creation"""
        # Remove the directory first
        shutil.rmtree(self.temp_dir)
        assert not os.path.exists(self.temp_dir)
        
        # Initialize downloader should create it
        self.downloader.ensure_output_dir()
        assert os.path.exists(self.temp_dir)
        assert os.path.isdir(self.temp_dir)
    
    @patch('subprocess.run')
    def test_check_ffmpeg_success(self, mock_subprocess):
        """Test successful ffmpeg check"""
        mock_subprocess.return_value = None
        result = self.downloader.check_ffmpeg()
        assert result is True
        mock_subprocess.assert_called_once()
    
    @patch('subprocess.run')
    def test_check_ffmpeg_failure(self, mock_subprocess):
        """Test failed ffmpeg check"""
        mock_subprocess.side_effect = FileNotFoundError()
        result = self.downloader.check_ffmpeg()
        assert result is False
    
    def test_get_next_file_number_empty_dir(self):
        """Test file numbering with empty directory"""
        result = self.downloader.get_next_file_number()
        assert result == 1
    
    def test_get_next_file_number_with_files(self):
        """Test file numbering with existing files"""
        # Create some test files
        test_files = ["001-test.mp4", "002-test.mp4", "005-test.mp3"]
        for filename in test_files:
            open(os.path.join(self.temp_dir, filename), 'w').close()
        
        result = self.downloader.get_next_file_number()
        assert result == 6  # Should be max(1,2,5) + 1
    
    def test_get_next_file_number_invalid_files(self):
        """Test file numbering with invalid filenames"""
        # Create files with invalid numbering
        test_files = ["invalid-test.mp4", "not-a-number-test.mp4", "test.mp4"]
        for filename in test_files:
            open(os.path.join(self.temp_dir, filename), 'w').close()
        
        result = self.downloader.get_next_file_number()
        assert result == 1  # Should default to 1
    
    def test_extract_formats(self):
        """Test format extraction from yt-dlp info"""
        mock_formats = [
            {'vcodec': 'avc1', 'height': 1080, 'format_id': 'test1080', 'ext': 'mp4', 'filesize': 100000},
            {'vcodec': 'avc1', 'height': 720, 'format_id': 'test720', 'ext': 'mp4', 'filesize': 50000},
            {'vcodec': 'none', 'height': None, 'format_id': 'audio_only', 'ext': 'mp3', 'filesize': 10000},  # Audio only
            {'vcodec': 'avc1', 'height': 1080, 'format_id': 'test1080_dup', 'ext': 'webm', 'filesize': 90000}  # Duplicate height
        ]
        
        result = self.downloader._extract_formats(mock_formats)
        
        # Should have 1080p, 720p, and audio-only (no duplicates)
        assert len(result) == 3
        
        # Check if qualities are correct
        qualities = [fmt['quality'] for fmt in result]
        assert '1080p' in qualities
        assert '720p' in qualities
        assert 'Audio Only (MP3)' in qualities
        
        # Should be sorted by quality (highest first)
        assert result[0]['quality'] == '1080p'
        assert result[1]['quality'] == '720p'
        assert result[2]['quality'] == 'Audio Only (MP3)'
    
    @patch('core.downloader.YoutubeDL')
    def test_get_video_info_success(self, mock_ytdl_class):
        """Test successful video info extraction"""
        mock_ytdl = MagicMock()
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        
        mock_info = {
            'title': 'Test Video',
            'duration': 180,
            'thumbnail': 'https://example.com/thumb.jpg',
            'formats': [
                {'vcodec': 'avc1', 'height': 720, 'format_id': 'test720', 'ext': 'mp4', 'filesize': 50000}
            ]
        }
        mock_ytdl.extract_info.return_value = mock_info
        
        result = self.downloader.get_video_info('https://youtube.com/watch?v=test')
        
        assert result['title'] == 'Test Video'
        assert result['duration'] == 180
        assert result['thumbnail'] == 'https://example.com/thumb.jpg'
        assert len(result['formats']) == 2  # 720p + Audio Only
    
    @patch('core.downloader.YoutubeDL')
    def test_get_video_info_error(self, mock_ytdl_class):
        """Test video info extraction error handling"""
        mock_ytdl = MagicMock()
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        mock_ytdl.extract_info.side_effect = Exception("Network error")
        
        result = self.downloader.get_video_info('https://invalid-url.com')
        
        assert 'error' in result
        assert 'Network error' in result['error']
    
    def test_download_m3u8_url(self):
        """Test m3u8 URL detection"""
        url = "https://example.com/stream.m3u8"
        
        with patch.object(self.downloader, '_download_m3u8') as mock_m3u8:
            mock_m3u8.return_value = {'success': True}
            result = self.downloader.download_video(url)
            mock_m3u8.assert_called_once()
            assert result['success'] is True
    
    def test_download_regular_url(self):
        """Test regular video URL"""
        url = "https://youtube.com/watch?v=test"
        
        with patch.object(self.downloader, '_download_with_ytdlp') as mock_ytdlp:
            mock_ytdlp.return_value = {'success': True}
            result = self.downloader.download_video(url, quality='720p')
            mock_ytdlp.assert_called_once_with(url, '720p', None)
            assert result['success'] is True
    
    @patch('subprocess.run')
    def test_download_m3u8_success(self, mock_subprocess):
        """Test successful m3u8 download"""
        mock_subprocess.return_value = None
        
        result = self.downloader._download_m3u8('https://example.com/stream.m3u8')
        
        assert result['success'] is True
        assert 'filename' in result
        # Should be called twice: once for ffmpeg check, once for download
        assert mock_subprocess.call_count == 2
    
    @patch('subprocess.run')
    @patch.object(VideoDownloader, 'check_ffmpeg')
    def test_download_m3u8_no_ffmpeg(self, mock_check_ffmpeg, mock_subprocess):
        """Test m3u8 download without ffmpeg"""
        mock_check_ffmpeg.return_value = False
        
        result = self.downloader._download_m3u8('https://example.com/stream.m3u8')
        
        assert result['success'] is False
        assert 'FFmpeg not found' in result['error']
        mock_subprocess.assert_not_called()
    
    @patch('core.downloader.YoutubeDL')
    def test_download_with_ytdlp_success(self, mock_ytdl_class):
        """Test successful yt-dlp download"""
        mock_ytdl = MagicMock()
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        mock_ytdl.download.return_value = None
        
        result = self.downloader._download_with_ytdlp('https://youtube.com/watch?v=test', '720p')
        
        assert result['success'] is True
        mock_ytdl.download.assert_called_once()
    
    @patch('core.downloader.YoutubeDL')
    def test_download_with_ytdlp_error(self, mock_ytdl_class):
        """Test yt-dlp download error"""
        mock_ytdl = MagicMock()
        mock_ytdl_class.return_value.__enter__.return_value = mock_ytdl
        mock_ytdl.download.side_effect = Exception("Download failed")
        
        result = self.downloader._download_with_ytdlp('https://youtube.com/watch?v=test', '720p')
        
        assert result['success'] is False
        assert 'Download failed' in result['error']
    
    def test_progress_hook_downloading(self):
        """Test progress hook during download"""
        progress_data = []
        
        def mock_callback(data):
            progress_data.append(data)
        
        self.downloader._progress_callback = mock_callback
        
        # Simulate yt-dlp progress data
        hook_data = {
            'status': 'downloading',
            '_percent_str': '50.0%',
            '_speed_str': '1.2MiB/s',
            'filename': '/path/to/video.mp4'
        }
        
        self.downloader._progress_hook(hook_data)
        
        assert len(progress_data) == 1
        assert progress_data[0]['status'] == 'downloading'
        assert progress_data[0]['percentage'] == '50.0%'
        assert progress_data[0]['speed'] == '1.2MiB/s'
    
    def test_progress_hook_finished(self):
        """Test progress hook when download finishes"""
        progress_data = []
        
        def mock_callback(data):
            progress_data.append(data)
        
        self.downloader._progress_callback = mock_callback
        
        hook_data = {
            'status': 'finished',
            'filename': '/path/to/video.mp4'
        }
        
        self.downloader._progress_hook(hook_data)
        
        assert len(progress_data) == 1
        assert progress_data[0]['status'] == 'finished'
        assert 'video.mp4' in progress_data[0]['filename']


if __name__ == '__main__':
    pytest.main([__file__])