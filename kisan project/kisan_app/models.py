from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta

# Create your models here.


class Farmer(models.Model):
    """Model representing a farmer in the Kisan system"""
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='farmer_profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    land_area = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="Area in acres")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def total_crops(self):
        return self.crops.count()
    
    @property
    def total_harvest_value(self):
        return sum(crop.total_value for crop in self.crops.all())
    
    @property
    def upcoming_harvests(self):
        today = date.today()
        return self.crops.filter(harvest_date__gte=today, harvest_date__lte=today + timedelta(days=30))


class CropCategory(models.Model):
    """Model for crop categories"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='🌾')
    
    class Meta:
        verbose_name_plural = "Crop Categories"
    
    def __str__(self):
        return self.name


class Crop(models.Model):
    """Model representing crops grown by farmers"""
    SEASON_CHOICES = [
        ('Kharif', 'Kharif (Monsoon)'),
        ('Rabi', 'Rabi (Winter)'),
        ('Zaid', 'Zaid (Summer)'),
        ('Annual', 'Annual'),
    ]
    
    STATUS_CHOICES = [
        ('Planted', 'Planted'),
        ('Growing', 'Growing'),
        ('Ready', 'Ready for Harvest'),
        ('Harvested', 'Harvested'),
        ('Sold', 'Sold'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(CropCategory, on_delete=models.SET_NULL, null=True, blank=True)
    season = models.CharField(max_length=50, choices=SEASON_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planted')
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='crops')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    planted_date = models.DateField(null=True, blank=True)
    harvest_date = models.DateField()
    actual_harvest_date = models.DateField(null=True, blank=True)
    investment_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.farmer.name}"
    
    @property
    def total_value(self):
        return self.quantity * self.price_per_kg
    
    @property
    def profit(self):
        return self.total_value - self.investment_cost
    
    @property
    def profit_margin(self):
        if self.investment_cost > 0:
            return (self.profit / self.investment_cost) * 100
        return 0
    
    @property
    def days_to_harvest(self):
        if self.harvest_date:
            delta = self.harvest_date - date.today()
            return delta.days
        return None
    
    @property
    def is_overdue(self):
        return self.harvest_date < date.today() and self.status not in ['Harvested', 'Sold']


class MarketPrice(models.Model):
    """Model for tracking market prices of crops"""
    crop_name = models.CharField(max_length=100)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    market_location = models.CharField(max_length=100)
    date_recorded = models.DateField(auto_now_add=True)
    source = models.CharField(max_length=100, default='Manual Entry')
    
    class Meta:
        ordering = ['-date_recorded']
    
    def __str__(self):
        return f"{self.crop_name} - ₹{self.price_per_kg} ({self.market_location})"


class WeatherData(models.Model):
    """Model for storing weather information"""
    location = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField(default=0.0)
    weather_condition = models.CharField(max_length=50)
    date_recorded = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_recorded']
    
    def __str__(self):
        return f"{self.location} - {self.weather_condition} ({self.date_recorded.date()})"


class Notification(models.Model):
    """Model for system notifications"""
    NOTIFICATION_TYPES = [
        ('harvest_reminder', 'Harvest Reminder'),
        ('price_alert', 'Price Alert'),
        ('weather_alert', 'Weather Alert'),
        ('general', 'General'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.farmer.name}"