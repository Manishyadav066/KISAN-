#!/usr/bin/env python
"""
Script to create sample data for the Kisan Project.
This script will populate the database with sample farmers, crops, and other data.
"""

import os
import sys
import django
from datetime import date, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_project.settings')
django.setup()

from django.contrib.auth.models import User
from kisan_app.models import Farmer, Crop, CropCategory, MarketPrice, WeatherData

def create_sample_data():
    """Create sample data for testing and development."""
    
    # Clear existing data
    print("Clearing existing data...")
    WeatherData.objects.all().delete()
    MarketPrice.objects.all().delete()
    Crop.objects.all().delete()
    Farmer.objects.all().delete()
    CropCategory.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    
    # Create crop categories
    print("Creating crop categories...")
    grains = CropCategory.objects.create(
        name="Grains",
        description="Cereal crops like wheat, rice, corn",
        icon="🌾"
    )
    
    vegetables = CropCategory.objects.create(
        name="Vegetables",
        description="Fresh vegetables and leafy greens",
        icon="🥬"
    )
    
    fruits = CropCategory.objects.create(
        name="Fruits",
        description="Fresh fruits and berries",
        icon="🍎"
    )
    
    pulses = CropCategory.objects.create(
        name="Pulses",
        description="Leguminous crops like lentils, beans",
        icon="🥜"
    )
    
    # Create sample users and farmers
    print("Creating sample farmers...")
    
    # Farmer 1
    user1 = User.objects.create_user(
        username="raj_kumar",
        email="raj.kumar@example.com",
        password="password123"
    )
    
    farmer1 = Farmer.objects.create(
        name="Raj Kumar",
        phone="9876543210",
        email="raj.kumar@example.com",
        address="123 Farm Road, Village ABC, State XYZ",
        user=user1,
        date_of_birth=date(1980, 5, 15),
        experience_years=15,
        land_area=12.5
    )
    
    # Farmer 2
    user2 = User.objects.create_user(
        username="priya_sharma",
        email="priya.sharma@example.com",
        password="password123"
    )
    
    farmer2 = Farmer.objects.create(
        name="Priya Sharma",
        phone="9876543211",
        email="priya.sharma@example.com",
        address="456 Green Field, Village DEF, State XYZ",
        user=user2,
        date_of_birth=date(1985, 8, 22),
        experience_years=10,
        land_area=8.2
    )
    
    # Farmer 3
    user3 = User.objects.create_user(
        username="amit_patel",
        email="amit.patel@example.com",
        password="password123"
    )
    
    farmer3 = Farmer.objects.create(
        name="Amit Patel",
        phone="9876543212",
        email="amit.patel@example.com",
        address="789 Harvest Lane, Village GHI, State XYZ",
        user=user3,
        date_of_birth=date(1975, 12, 3),
        experience_years=20,
        land_area=25.0
    )
    
    # Create sample crops
    print("Creating sample crops...")
    
    # Crops for Raj Kumar
    Crop.objects.create(
        name="Wheat",
        category=grains,
        season="Rabi",
        status="Harvested",
        price_per_kg=22.5,
        farmer=farmer1,
        quantity=1500,
        planted_date=date(2024, 10, 15),
        harvest_date=date(2025, 3, 15),
        actual_harvest_date=date(2025, 3, 10),
        investment_cost=25000,
        notes="High yield variety, good quality"
    )
    
    Crop.objects.create(
        name="Tomatoes",
        category=vegetables,
        season="Kharif",
        status="Growing",
        price_per_kg=35.0,
        farmer=farmer1,
        quantity=800,
        planted_date=date(2025, 5, 1),
        harvest_date=date(2025, 8, 1),
        investment_cost=15000,
        notes="Greenhouse cultivation"
    )
    
    # Crops for Priya Sharma
    Crop.objects.create(
        name="Rice",
        category=grains,
        season="Kharif",
        status="Planted",
        price_per_kg=28.0,
        farmer=farmer2,
        quantity=2000,
        planted_date=date(2025, 6, 10),
        harvest_date=date(2025, 10, 10),
        investment_cost=30000,
        notes="Organic farming method"
    )
    
    Crop.objects.create(
        name="Mangoes",
        category=fruits,
        season="Annual",
        status="Growing",
        price_per_kg=80.0,
        farmer=farmer2,
        quantity=500,
        planted_date=date(2023, 7, 15),
        harvest_date=date(2026, 5, 15),
        investment_cost=50000,
        notes="Premium variety, 3rd year tree"
    )
    
    # Crops for Amit Patel
    Crop.objects.create(
        name="Lentils",
        category=pulses,
        season="Rabi",
        status="Ready",
        price_per_kg=65.0,
        farmer=farmer3,
        quantity=1200,
        planted_date=date(2024, 11, 1),
        harvest_date=date(2025, 3, 1),
        investment_cost=18000,
        notes="High protein content"
    )
    
    Crop.objects.create(
        name="Potatoes",
        category=vegetables,
        season="Zaid",
        status="Harvested",
        price_per_kg=25.0,
        farmer=farmer3,
        quantity=3000,
        planted_date=date(2025, 3, 1),
        harvest_date=date(2025, 6, 1),
        actual_harvest_date=date(2025, 5, 28),
        investment_cost=22000,
        notes="Early variety, good market price"
    )
    
    # Create sample market prices
    print("Creating sample market prices...")
    
    MarketPrice.objects.create(
        crop_name="Wheat",
        price_per_kg=24.0,
        market_location="Mumbai",
        source="Government Market"
    )
    
    MarketPrice.objects.create(
        crop_name="Wheat",
        price_per_kg=23.5,
        market_location="Delhi",
        source="Wholesale Market"
    )
    
    MarketPrice.objects.create(
        crop_name="Rice",
        price_per_kg=30.0,
        market_location="Chennai",
        source="Government Market"
    )
    
    MarketPrice.objects.create(
        crop_name="Tomatoes",
        price_per_kg=40.0,
        market_location="Bangalore",
        source="Retail Market"
    )
    
    MarketPrice.objects.create(
        crop_name="Mangoes",
        price_per_kg=85.0,
        market_location="Mumbai",
        source="Fruit Market"
    )
    
    MarketPrice.objects.create(
        crop_name="Lentils",
        price_per_kg=70.0,
        market_location="Delhi",
        source="Wholesale Market"
    )
    
    # Create sample weather data
    print("Creating sample weather data...")
    
    locations = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]
    conditions = ["Sunny", "Rainy", "Cloudy", "Partly Cloudy", "Overcast"]
    
    for i in range(20):
        WeatherData.objects.create(
            location=locations[i % len(locations)],
            temperature=25.0 + (i % 15),
            humidity=40.0 + (i % 40),
            rainfall=0.0 + (i % 10),
            weather_condition=conditions[i % len(conditions)]
        )
    
    print("Sample data creation completed successfully!")

if __name__ == "__main__":
    create_sample_data()