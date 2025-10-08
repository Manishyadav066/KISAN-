#!/usr/bin/env python
"""
Script to create a superuser for the Kisan Project.
This script will create a default superuser account.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_project.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    """Create a default superuser account."""
    User = get_user_model()
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("Superuser already exists!")
        return
    
    # Create superuser
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    
    try:
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("Please change the password after first login!")
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == "__main__":
    create_superuser()