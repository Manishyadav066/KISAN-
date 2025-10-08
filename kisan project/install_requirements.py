#!/usr/bin/env python
"""
Script to install requirements for the Kisan Project.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install requirements from requirements.txt file."""
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("ERROR: requirements.txt file not found in current directory")
        print("Please make sure you're running this script from the project root directory")
        return False
    
    try:
        # Install requirements
        print("Installing requirements from requirements.txt...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Requirements installed successfully!")
            print(result.stdout)
            return True
        else:
            print("Error installing requirements:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Error running pip install: {e}")
        return False

if __name__ == "__main__":
    success = install_requirements()
    if not success:
        sys.exit(1)