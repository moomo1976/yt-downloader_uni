#!/usr/bin/env python3
"""
Standalone dependency checker script
Run this to verify all required components are installed
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.dependency_checker import print_dependency_status, DependencyChecker

def main():
    """Main function to check dependencies"""
    try:
        print("🎥 YouTube Downloader Pro - Kontrola závislostí")
    except UnicodeEncodeError:
        print("YouTube Downloader Pro - Kontrola zavislosti")
    print("=" * 60)
    print()
    
    # Print detailed status
    print_dependency_status()
    
    # Quick summary
    checker = DependencyChecker()
    results = checker.check_all_dependencies()
    
    print("\n" + "=" * 60)
    if results['all_ok']:
        try:
            print("✅ VÝSLEDEK: Aplikace je připravena k použití!")
        except UnicodeEncodeError:
            print("VYSLEDEK: Aplikace je pripravena k pouziti!")
        sys.exit(0)
    else:
        try:
            print("❌ VÝSLEDEK: Některé komponenty chybí!")
            print("\n🔧 DOPORUČENÉ KROKY:")
        except UnicodeEncodeError:
            print("VYSLEDEK: Nektere komponenty chybi!")
            print("\nDOPORUCENE KROKY:")
        
        # Show installation commands
        commands = checker.get_installation_commands()
        if commands:
            print("\n1. Nainstalujte chybějící Python balíčky:")
            for cmd in commands:
                print(f"   {cmd}")
        
        # Check for system dependencies
        ffmpeg_missing = False
        for dep_name, info in results['system'].items():
            if not info['available'] and info['required']:
                ffmpeg_missing = True
                print(f"\n2. Nainstalujte {dep_name}:")
                print(f"   {info['install_info']}")
        
        if not ffmpeg_missing and commands:
            print("\n2. Restartujte aplikaci")
        
        sys.exit(1)

if __name__ == "__main__":
    main()