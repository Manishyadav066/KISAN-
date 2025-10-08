from django.contrib import admin
from .models import Farmer, Crop, CropCategory, MarketPrice, WeatherData, Notification

# Register your models here.


@admin.register(CropCategory)
class CropCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name']


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'land_area', 'experience_years', 'total_crops', 'created_at']
    list_filter = ['created_at', 'experience_years']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at', 'total_crops', 'total_harvest_value']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'phone', 'email', 'address')
        }),
        ('Profile Details', {
            'fields': ('profile_picture', 'date_of_birth', 'experience_years', 'land_area')
        }),
        ('System Information', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('total_crops', 'total_harvest_value'),
            'classes': ('collapse',)
        })
    )


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'category', 'season', 'status', 'quantity', 'price_per_kg', 'total_value', 'harvest_date', 'days_to_harvest']
    list_filter = ['season', 'status', 'category', 'harvest_date', 'created_at']
    search_fields = ['name', 'farmer__name']
    readonly_fields = ['created_at', 'total_value', 'profit', 'profit_margin', 'days_to_harvest', 'is_overdue']
    date_hierarchy = 'harvest_date'
    
    fieldsets = (
        ('Crop Information', {
            'fields': ('name', 'category', 'farmer', 'season', 'status')
        }),
        ('Planting & Harvest', {
            'fields': ('planted_date', 'harvest_date', 'actual_harvest_date')
        }),
        ('Financial Details', {
            'fields': ('quantity', 'price_per_kg', 'investment_cost', 'total_value', 'profit', 'profit_margin')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('created_at', 'days_to_harvest', 'is_overdue'),
            'classes': ('collapse',)
        })
    )


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop_name', 'price_per_kg', 'market_location', 'date_recorded', 'source']
    list_filter = ['market_location', 'date_recorded', 'source']
    search_fields = ['crop_name', 'market_location']
    date_hierarchy = 'date_recorded'


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'weather_condition', 'temperature', 'humidity', 'rainfall', 'date_recorded']
    list_filter = ['location', 'weather_condition', 'date_recorded']
    search_fields = ['location']
    date_hierarchy = 'date_recorded'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'farmer', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'farmer__name']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'