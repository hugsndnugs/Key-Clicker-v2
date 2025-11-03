#!/usr/bin/env python3
"""
Build script for creating executable from Auto Key Clicker
"""

import PyInstaller.__main__
import os
import shutil

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Clean previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # PyInstaller arguments
    args = [
        'key_clicker.py',
        '--name=AutoKeyClicker',
        '--onefile',
        '--windowed',
        '--icon=NONE',  # Can add icon file path here if available
        '--add-data=requirements.txt;.' if os.name == 'nt' else '--add-data=requirements.txt:.',
        '--hidden-import=pynput',
        '--hidden-import=pystray',
        '--hidden-import=PIL',
        '--collect-all=pynput',
        '--collect-all=pystray',
    ]
    
    print("Building executable...")
    print(f"Command: pyinstaller {' '.join(args)}")
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✓ Build completed successfully!")
        print(f"Executable location: dist/AutoKeyClicker{' considering OS-specific extension'}")
    except Exception as e:
        print(f"\n✗ Build failed: {e}")
        raise


if __name__ == "__main__":
    build_executable()


