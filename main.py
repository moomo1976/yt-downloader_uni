#!/usr/bin/env python3
"""
YouTube Downloader Pro v2.1.0 - Main Entry Point
Modern YouTube video downloader with GUI and dependency checking
"""
import sys
import os

# Add project root and src to path
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

def main():
    """Main application entry point with error handling"""
    try:
        from version import APP_TITLE, VERSION
        print(f"Starting {APP_TITLE}...")
        
        from gui.simple_gui import main as run_gui
        run_gui()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install required packages:")
        print("pip install -r requirements.txt")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()