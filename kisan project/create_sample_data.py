#!/usr/bin/env python
import os
import sys
import django
from datetime import date, datetime

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_project.settings')
django.setup()

from kisan_app.models import Farmer, Crop

# Create sample farmers
farmers_data = [
    {
        'name': 'Ramesh Kumar',
        'phone': '+91 9876543210',
        'email': 'ramesh.kumar@email.com',
        'address': 'Village Ramnagar, District Rajasthan, Pin: 302001'
    },
    {
        'name': 'Sunita Devi',
        'phone': '+91 9876543211',
        'email': 'sunita.devi@email.com',
        'address': 'Village Krishnanagar, District Punjab, Pin: 144001'
    },
    {
        'name': 'Mohan Sharma',
        'phone': '+91 9876543212',
        'email': '',
        'address': 'Village Gokul, District Uttar Pradesh, Pin: 281001'
    },
    {
        'name': 'Lakshmi Patel',
        'phone': '+91 9876543213',
        'email': 'lakshmi.patel@email.com',
        'address': 'Village Anand, District Gujarat, Pin: 388001'
    }
]

# Create sample crops
crops_data = [
    {
        'name': 'Wheat',
        'season': 'Rabi',
        'price_per_kg': 25.50,
        'quantity': 500.00,
        'harvest_date': date(2024, 4, 15)
    },
    {
        'name': 'Rice',
        'season': 'Kharif',
        'price_per_kg': 30.00,
        'quantity': 750.00,
        'harvest_date': date(2024, 10, 20)
    },
    {
        'name': 'Cotton',
        'season': 'Kharif',
        'price_per_kg': 85.00,
        'quantity': 200.00,
        'harvest_date': date(2024, 11, 5)
    },
    {
        'name': 'Sugarcane',
        'season': 'Annual',
        'price_per_kg': 3.50,
        'quantity': 2000.00,
        'harvest_date': date(2024, 12, 10)
    }
]

print("Creating sample farmers...")
farmers = []
for farmer_data in farmers_data:
    farmer, created = Farmer.objects.get_or_create(
        name=farmer_data['name'],
        defaults=farmer_data
    )
    if created:
        print(f"✓ Created farmer: {farmer.name}")
    else:
        print(f"• Farmer already exists: {farmer.name}")
    farmers.append(farmer)

print("\nCreating sample crops...")
for i, crop_data in enumerate(crops_data):
    crop_data['farmer'] = farmers[i % len(farmers)]  # Assign farmers cyclically
    crop, created = Crop.objects.get_or_create(
        name=crop_data['name'],
        farmer=crop_data['farmer'],
        defaults=crop_data
    )
    if created:
        print(f"✓ Created crop: {crop.name} for {crop.farmer.name}")
    else:
        print(f"• Crop already exists: {crop.name} for {crop.farmer.name}")

print(f"\n🌾 Sample data creation complete!")
print(f"📊 Total Farmers: {Farmer.objects.count()}")
print(f"🌱 Total Crops: {Crop.objects.count()}")
print("\n🚀 You can now visit your website to see the beautiful new design with sample data!")