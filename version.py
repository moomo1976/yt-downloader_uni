"""Version information for YouTube Downloader Pro"""

__version__ = "2.1.0"
__version_info__ = (2, 1, 0)

VERSION = __version__
APP_NAME = "YouTube Downloader Pro"
APP_TITLE = f"{APP_NAME} v{VERSION}"

# Changelog for this version
CHANGELOG = """
Version 2.1.0 (2025-09-06):
✅ NEW: Automatická kontrola závislostí při spuštění
✅ NEW: Systém ověření FFmpeg a Python balíčků  
✅ NEW: Varovná okna pro chybějící komponenty
✅ NEW: Menu "Nástroje" s kontrolou závislostí
✅ NEW: Standalone skript check_dependencies.py
✅ FIX: Lepší zpracování Unicode znaků na Windows
✅ FIX: Robustnější progress tracking
✅ DOCS: Přidána dokumentace DEPENDENCY_CHECK.md
"""