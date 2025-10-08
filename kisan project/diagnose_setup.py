#!/usr/bin/env python
"""
Diagnostic script for Kisan Project setup.
"""

import os
import sys

def diagnose_setup():
    """Diagnose the current setup and environment."""
    print("=== Kisan Project Setup Diagnosis ===")
    print()
    
    # Current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    # List files in current directory
    print("\nFiles in current directory:")
    files = os.listdir('.')
    for file in files:
        print(f"  {file}")
    
    # Check if requirements.txt exists
    print("\nChecking for requirements.txt:")
    if os.path.exists('requirements.txt'):
        print("  ✓ requirements.txt found")
        # Check file size
        size = os.path.getsize('requirements.txt')
        print(f"  File size: {size} bytes")
        
        # Show first few lines
        try:
            with open('requirements.txt', 'r') as f:
                lines = f.readlines()
                print("  First 5 lines:")
                for i, line in enumerate(lines[:5]):
                    print(f"    {i+1}: {line.strip()}")
        except Exception as e:
            print(f"  Error reading file: {e}")
    else:
        print("  ✗ requirements.txt NOT found")
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Check if we're in a virtual environment
    print("\nVirtual environment check:")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("  ✓ Virtual environment is active")
    else:
        print("  ⚠ No virtual environment detected")
        print("    Consider creating one with: python -m venv venv")
    
    print("\n=== Diagnosis Complete ===")

if __name__ == "__main__":
    diagnose_setup()