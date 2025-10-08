#!/usr/bin/env python
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create test client
client = Client()

try:
    # Test weather page
    print("Testing weather page...")
    response = client.get('/weather/')
    print(f"Weather page status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Weather page is working correctly!")
    else:
        print(f"❌ Weather page failed with status: {response.status_code}")
        print(f"Response content: {response.content.decode()[:500]}...")
        
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print(f"Error type: {type(e).__name__}")