"""
Dependency Verification System
Checks if required components are installed and available
"""
import subprocess
import sys
import os
import shutil
from typing import Dict, List, Optional, Tuple
import importlib.util


class DependencyChecker:
    """Checks system and Python dependencies"""
    
    def __init__(self):
        self.system_deps = {
            'ffmpeg': {
                'command': ['ffmpeg', '-version'],
                'description': 'FFmpeg - pro zpracování video souborů',
                'install_info': 'Stáhněte z https://ffmpeg.org/download.html',
                'required': True
            }
        }
        
        self.python_deps = {
            'yt_dlp': {
                'package': 'yt-dlp',
                'description': 'yt-dlp - pro stahování YouTube videí',
                'required': True
            },
            'customtkinter': {
                'package': 'customtkinter',
                'description': 'CustomTkinter - pro moderní GUI',
                'required': True
            },
            'PIL': {
                'package': 'Pillow',
                'description': 'Pillow - pro práci s obrázky',
                'required': True
            },
            'requests': {
                'package': 'requests',
                'description': 'Requests - pro HTTP požadavky',
                'required': True
            }
        }
    
    def check_system_dependency(self, dep_name: str) -> Tuple[bool, str]:
        """Check if system dependency is available"""
        dep_info = self.system_deps.get(dep_name)
        if not dep_info:
            return False, f"Neznámá závislost: {dep_name}"
        
        try:
            # First try to find the executable in PATH
            if shutil.which(dep_name):
                # Then verify it works by running the command
                result = subprocess.run(
                    dep_info['command'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=10
                )
                if result.returncode == 0:
                    return True, f"✅ {dep_name} je dostupný"
                else:
                    return False, f"❌ {dep_name} nenastartoval správně"
            else:
                return False, f"❌ {dep_name} nebyl nalezen v PATH"
                
        except subprocess.TimeoutExpired:
            return False, f"❌ {dep_name} neodpověděl včas"
        except FileNotFoundError:
            return False, f"❌ {dep_name} nebyl nalezen"
        except Exception as e:
            return False, f"❌ Chyba při testování {dep_name}: {str(e)}"
    
    def check_python_dependency(self, module_name: str) -> Tuple[bool, str]:
        """Check if Python module is available"""
        dep_info = self.python_deps.get(module_name)
        if not dep_info:
            return False, f"Neznámá Python závislost: {module_name}"
        
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                return False, f"❌ {dep_info['package']} není nainstalován"
            
            # Try to actually import the module
            module = importlib.import_module(module_name)
            
            # Additional checks for specific modules
            if module_name == 'yt_dlp':
                # Check if yt-dlp has basic functionality
                from yt_dlp import YoutubeDL
                return True, f"✅ {dep_info['package']} je dostupný"
            elif module_name == 'customtkinter':
                # Check if customtkinter can be imported
                import customtkinter
                return True, f"✅ {dep_info['package']} je dostupný"
            else:
                return True, f"✅ {dep_info['package']} je dostupný"
                
        except ImportError as e:
            return False, f"❌ {dep_info['package']} nelze importovat: {str(e)}"
        except Exception as e:
            return False, f"❌ Chyba při testování {dep_info['package']}: {str(e)}"
    
    def check_all_dependencies(self) -> Dict[str, Dict]:
        """Check all dependencies and return detailed results"""
        results = {
            'system': {},
            'python': {},
            'all_ok': True,
            'critical_missing': [],
            'warnings': []
        }
        
        # Check system dependencies
        for dep_name, dep_info in self.system_deps.items():
            is_ok, message = self.check_system_dependency(dep_name)
            results['system'][dep_name] = {
                'available': is_ok,
                'message': message,
                'description': dep_info['description'],
                'install_info': dep_info['install_info'],
                'required': dep_info['required']
            }
            
            if not is_ok and dep_info['required']:
                results['all_ok'] = False
                results['critical_missing'].append(dep_name)
        
        # Check Python dependencies
        for module_name, dep_info in self.python_deps.items():
            is_ok, message = self.check_python_dependency(module_name)
            results['python'][module_name] = {
                'available': is_ok,
                'message': message,
                'description': dep_info['description'],
                'package': dep_info['package'],
                'required': dep_info['required']
            }
            
            if not is_ok and dep_info['required']:
                results['all_ok'] = False
                results['critical_missing'].append(dep_info['package'])
        
        return results
    
    def get_missing_dependencies_report(self) -> str:
        """Generate a detailed report of missing dependencies"""
        results = self.check_all_dependencies()
        
        if results['all_ok']:
            return "✅ Všechny požadované komponenty jsou dostupné!"
        
        report = ["❌ CHYBĚJÍCÍ KOMPONENTY:", ""]
        
        # System dependencies
        for dep_name, info in results['system'].items():
            if not info['available'] and info['required']:
                report.append(f"🔧 {info['description']}")
                report.append(f"   Problém: {info['message']}")
                report.append(f"   Řešení: {info['install_info']}")
                report.append("")
        
        # Python dependencies  
        python_missing = []
        for module_name, info in results['python'].items():
            if not info['available'] and info['required']:
                python_missing.append(info['package'])
                report.append(f"🐍 {info['description']}")
                report.append(f"   Problém: {info['message']}")
                report.append(f"   Řešení: pip install {info['package']}")
                report.append("")
        
        # Summary installation command
        if python_missing:
            report.append("💡 RYCHLÁ INSTALACE PYTHON BALÍČKŮ:")
            report.append(f"   pip install {' '.join(python_missing)}")
            report.append("")
        
        return "\n".join(report)
    
    def get_installation_commands(self) -> List[str]:
        """Get list of installation commands for missing dependencies"""
        results = self.check_all_dependencies()
        commands = []
        
        python_missing = []
        for module_name, info in results['python'].items():
            if not info['available'] and info['required']:
                python_missing.append(info['package'])
        
        if python_missing:
            commands.append(f"pip install {' '.join(python_missing)}")
        
        return commands


def quick_check() -> bool:
    """Quick check if all critical dependencies are available"""
    checker = DependencyChecker()
    results = checker.check_all_dependencies()
    return results['all_ok']


def print_dependency_status():
    """Print current dependency status to console"""
    checker = DependencyChecker()
    try:
        print("🔍 Kontrola závislostí...")
        print("=" * 50)
        
        results = checker.check_all_dependencies()
        
        # Print system dependencies
        print("🔧 SYSTÉMOVÉ KOMPONENTY:")
        for dep_name, info in results['system'].items():
            print(f"   {info['message']}")
        print()
        
        # Print Python dependencies
        print("🐍 PYTHON BALÍČKY:")
        for module_name, info in results['python'].items():
            print(f"   {info['message']}")
        print()
        
        if not results['all_ok']:
            print("❌ ŘEŠENÍ PROBLÉMŮ:")
            print(checker.get_missing_dependencies_report())
        else:
            print("✅ Všechny komponenty jsou v pořádku!")
    except UnicodeEncodeError:
        # Fallback for systems with encoding issues
        print("Kontrola zavislosti...")
        print("=" * 50)
        
        results = checker.check_all_dependencies()
        
        print("SYSTEMOVE KOMPONENTY:")
        for dep_name, info in results['system'].items():
            clean_msg = info['message'].encode('ascii', errors='ignore').decode('ascii')
            print(f"   {clean_msg}")
        print()
        
        print("PYTHON BALICKY:")
        for module_name, info in results['python'].items():
            clean_msg = info['message'].encode('ascii', errors='ignore').decode('ascii')
            print(f"   {clean_msg}")
        print()
        
        if not results['all_ok']:
            print("RESENI PROBLEMU:")
            report = checker.get_missing_dependencies_report()
            clean_report = report.encode('ascii', errors='ignore').decode('ascii')
            print(clean_report)
        else:
            print("Vsechny komponenty jsou v poradku!")


if __name__ == "__main__":
    print_dependency_status()