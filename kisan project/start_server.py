#!/usr/bin/env python
"""
Startup script for the Kisan Project.
This script will handle initial setup and start the development server.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_project():
    """Setup the project by running migrations and creating sample data."""
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_project.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    print("Setting up the Kisan Project...")
    
    # Run migrations
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("Setup completed successfully!")

def start_server():
    """Start the development server."""
    from django.core.management import execute_from_command_line
    print("Starting development server...")
    execute_from_command_line(['manage.py', 'runserver'])

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_project()
    else:
        start_server()