#!/usr/bin/env python
import os
import sys
import django
from datetime import date, datetime, timedelta
import random

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_project.settings')
django.setup()

from kisan_app.models import Farmer, Crop, CropCategory, MarketPrice, WeatherData, Notification

# Create crop categories
categories_data = [
    {'name': 'Cereals', 'description': 'Grains like wheat, rice, corn', 'icon': '🌾'},
    {'name': 'Pulses', 'description': 'Legumes like lentils, chickpeas', 'icon': '🫘'},
    {'name': 'Cash Crops', 'description': 'Cotton, sugarcane, tobacco', 'icon': '💰'},
    {'name': 'Fruits', 'description': 'Seasonal and perennial fruits', 'icon': '🍎'},
    {'name': 'Vegetables', 'description': 'Fresh vegetables and greens', 'icon': '🥬'},
    {'name': 'Spices', 'description': 'Herbs and spices', 'icon': '🌶️'},
]

print("Creating crop categories...")
for cat_data in categories_data:
    category, created = CropCategory.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"✓ Created category: {category.name}")

# Update existing farmers with additional data
print("\nUpdating farmer profiles...")
farmers = Farmer.objects.all()
for i, farmer in enumerate(farmers):
    farmer.experience_years = random.randint(1, 25)
    farmer.land_area = round(random.uniform(0.5, 50.0), 2)
    farmer.date_of_birth = date(1960 + random.randint(0, 40), random.randint(1, 12), random.randint(1, 28))
    farmer.save()
    print(f"✓ Updated farmer: {farmer.name} ({farmer.experience_years} years exp, {farmer.land_area} acres)")

# Update existing crops with additional data
print("\nUpdating crop data...")
categories = list(CropCategory.objects.all())
crop_statuses = ['Planted', 'Growing', 'Ready', 'Harvested', 'Sold']

crops = Crop.objects.all()
for crop in crops:
    crop.category = random.choice(categories)
    crop.status = random.choice(crop_statuses)
    crop.investment_cost = round(random.uniform(1000, 10000), 2)
    crop.planted_date = crop.harvest_date - timedelta(days=random.randint(60, 150))
    
    if crop.status in ['Harvested', 'Sold']:
        crop.actual_harvest_date = crop.harvest_date + timedelta(days=random.randint(-5, 10))
    
    crop.notes = f"Quality: {'High' if random.random() > 0.5 else 'Medium'}, Weather: {'Favorable' if random.random() > 0.3 else 'Challenging'}"
    crop.save()
    print(f"✓ Updated crop: {crop.name} ({crop.status}, ₹{crop.investment_cost})")

# Create additional advanced crops
advanced_crops_data = [
    {'name': 'Basmati Rice', 'category': 'Cereals', 'season': 'Kharif', 'price': 45.0, 'quantity': 600},
    {'name': 'Organic Wheat', 'category': 'Cereals', 'season': 'Rabi', 'price': 35.0, 'quantity': 800},
    {'name': 'Chili Peppers', 'category': 'Spices', 'season': 'Kharif', 'price': 120.0, 'quantity': 150},
    {'name': 'Mango (Alphonso)', 'category': 'Fruits', 'season': 'Annual', 'price': 200.0, 'quantity': 300},
    {'name': 'Organic Tomatoes', 'category': 'Vegetables', 'season': 'Rabi', 'price': 25.0, 'quantity': 400},
    {'name': 'Turmeric', 'category': 'Spices', 'season': 'Kharif', 'price': 180.0, 'quantity': 100},
]

print("\nCreating advanced crops...")
for crop_data in advanced_crops_data:
    category = CropCategory.objects.get(name=crop_data['category'])
    farmer = random.choice(farmers)
    
    harvest_date = date.today() + timedelta(days=random.randint(-30, 90))
    planted_date = harvest_date - timedelta(days=random.randint(60, 150))
    
    crop, created = Crop.objects.get_or_create(
        name=crop_data['name'],
        farmer=farmer,
        defaults={
            'category': category,
            'season': crop_data['season'],
            'price_per_kg': crop_data['price'],
            'quantity': crop_data['quantity'],
            'harvest_date': harvest_date,
            'planted_date': planted_date,
            'status': random.choice(crop_statuses),
            'investment_cost': round(crop_data['price'] * crop_data['quantity'] * 0.3, 2),
            'notes': f"Premium quality {crop_data['name']} with excellent market demand"
        }
    )
    if created:
        print(f"✓ Created advanced crop: {crop.name} for {crop.farmer.name}")

# Create market price data
print("\nCreating market price data...")
market_locations = ['Delhi Mandi', 'Mumbai APMC', 'Pune Market', 'Bangalore Market', 'Chennai Wholesale']
crop_names = ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Tomatoes', 'Onions', 'Potatoes', 'Chili', 'Turmeric']

for crop_name in crop_names:
    for location in market_locations:
        base_price = random.uniform(15, 200)
        for days_ago in range(0, 15):
            price_variation = base_price * random.uniform(0.9, 1.1)
            date_recorded = date.today() - timedelta(days=days_ago)
            
            market_price, created = MarketPrice.objects.get_or_create(
                crop_name=crop_name,
                market_location=location,
                date_recorded=date_recorded,
                defaults={
                    'price_per_kg': round(price_variation, 2),
                    'source': 'Market Survey' if random.random() > 0.5 else 'Government Data'
                }
            )
            if created:
                print(f"✓ Added price: {crop_name} - ₹{market_price.price_per_kg}/kg ({location})")

# Create weather data
print("\nCreating weather data...")
locations = ['Delhi', 'Mumbai', 'Pune', 'Bangalore', 'Chennai', 'Ahmedabad', 'Jaipur', 'Lucknow']
weather_conditions = ['Sunny', 'Cloudy', 'Rainy', 'Overcast', 'Partly Cloudy', 'Clear']

for location in locations:
    for days_ago in range(0, 10):
        date_recorded = datetime.now() - timedelta(days=days_ago)
        
        weather, created = WeatherData.objects.get_or_create(
            location=location,
            date_recorded=date_recorded,
            defaults={
                'temperature': round(random.uniform(15, 40), 1),
                'humidity': round(random.uniform(30, 90), 1),
                'rainfall': round(random.uniform(0, 50), 1),
                'weather_condition': random.choice(weather_conditions)
            }
        )
        if created:
            print(f"✓ Added weather: {location} - {weather.weather_condition} ({weather.temperature}°C)")

# Create notifications
print("\nCreating notifications...")
notification_types = ['harvest_reminder', 'price_alert', 'weather_alert', 'general']

for farmer in farmers:
    # Harvest reminders
    upcoming_crops = farmer.crops.filter(
        harvest_date__gte=date.today(),
        harvest_date__lte=date.today() + timedelta(days=7)
    )
    
    for crop in upcoming_crops:
        notification, created = Notification.objects.get_or_create(
            farmer=farmer,
            title=f"Harvest Reminder: {crop.name}",
            defaults={
                'message': f"Your {crop.name} crop is scheduled for harvest on {crop.harvest_date.strftime('%B %d, %Y')}. Please prepare for harvesting activities.",
                'notification_type': 'harvest_reminder',
                'is_read': random.choice([True, False])
            }
        )
        if created:
            print(f"✓ Created notification: {notification.title}")
    
    # General notifications
    general_messages = [
        "New government subsidies available for organic farming",
        "Weather alert: Heavy rains expected in your area",
        "Market prices for wheat have increased by 10%",
        "Training program on modern farming techniques available",
        "Soil testing camp organized in your district"
    ]
    
    message = random.choice(general_messages)
    notification, created = Notification.objects.get_or_create(
        farmer=farmer,
        title="Important Update",
        message=message,
        defaults={
            'notification_type': random.choice(notification_types),
            'is_read': random.choice([True, False])
        }
    )
    if created:
        print(f"✓ Created general notification for {farmer.name}")

print(f"\n🎉 Advanced data creation complete!")
print(f"📊 Statistics:")
print(f"   - Total Farmers: {Farmer.objects.count()}")
print(f"   - Total Crops: {Crop.objects.count()}")
print(f"   - Crop Categories: {CropCategory.objects.count()}")
print(f"   - Market Prices: {MarketPrice.objects.count()}")
print(f"   - Weather Records: {WeatherData.objects.count()}")
print(f"   - Notifications: {Notification.objects.count()}")
print(f"\n🚀 Your Kisan Project now has advanced features with comprehensive data!")