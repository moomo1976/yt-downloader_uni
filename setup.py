"""
Setup script for YT Downloader Pro
"""
from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="yt-downloader-pro",
    version="1.0.0",
    author="moomo1976",
    description="Modern YouTube video downloader with quality selection and progress tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moomo1976/yt-downloader_uni",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "yt-downloader-pro=gui.modern_gui:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)