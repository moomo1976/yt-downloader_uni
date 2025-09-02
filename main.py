#!/usr/bin/env python3
"""
YT Downloader Pro - Main Entry Point
Modern YouTube video downloader with GUI
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.modern_gui import main

if __name__ == "__main__":
    main()