from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import date, timedelta
import json
from .models import Farmer, Crop, CropCategory, MarketPrice, WeatherData, Notification

# Create your views here.


def home(request):
    """Enhanced home page view with analytics"""
    farmers_count = Farmer.objects.count()
    crops_count = Crop.objects.count()
    
    # Analytics data
    total_harvest_value = Crop.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_investment = Crop.objects.aggregate(total=Sum('investment_cost'))['total'] or 0
    total_profit = sum(crop.profit for crop in Crop.objects.all())
    
    # Recent activities
    recent_crops = Crop.objects.order_by('-created_at')[:5]
    upcoming_harvests = Crop.objects.filter(
        harvest_date__gte=date.today(),
        harvest_date__lte=date.today() + timedelta(days=30),
        status__in=['Planted', 'Growing']
    ).order_by('harvest_date')[:5]
    
    # Crop distribution by season
    season_stats = Crop.objects.values('season').annotate(count=Count('id'))
    
    # Top performing farmers
    top_farmers = Farmer.objects.annotate(
        total_value=Sum('crops__quantity')
    ).order_by('-total_value')[:3]
    
    context = {
        'farmers_count': farmers_count,
        'crops_count': crops_count,
        'total_harvest_value': total_harvest_value,
        'total_investment': total_investment,
        'total_profit': total_profit,
        'recent_crops': recent_crops,
        'upcoming_harvests': upcoming_harvests,
        'season_stats': season_stats,
        'top_farmers': top_farmers,
    }
    
    return render(request, 'kisan_app/home.html', context)


def farmers_list(request):
    """Enhanced farmers list with search and filtering"""
    farmers = Farmer.objects.all().prefetch_related('crops')
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        farmers = farmers.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(address__icontains=search)
        )
    
    # Filter by experience
    experience = request.GET.get('experience')
    if experience:
        if experience == 'new':
            farmers = farmers.filter(experience_years__lt=2)
        elif experience == 'experienced':
            farmers = farmers.filter(experience_years__gte=2, experience_years__lt=10)
        elif experience == 'expert':
            farmers = farmers.filter(experience_years__gte=10)
    
    # Add analytics for each farmer
    for farmer in farmers:
        farmer.crop_count = farmer.crops.count()
        farmer.total_value = sum(crop.total_value for crop in farmer.crops.all())
        farmer.upcoming_count = farmer.upcoming_harvests.count()
    
    context = {
        'farmers': farmers,
        'search': search,
        'experience': experience,
    }
    
    return render(request, 'kisan_app/farmers_list.html', context)


def farmer_detail(request, farmer_id):
    """Detailed farmer profile with analytics"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    # Farmer analytics
    total_crops = farmer.crops.count()
    total_value = farmer.total_harvest_value
    upcoming_harvests = farmer.upcoming_harvests
    
    # Crop distribution
    crop_by_season = farmer.crops.values('season').annotate(count=Count('id'))
    crop_by_status = farmer.crops.values('status').annotate(count=Count('id'))
    
    # Recent activities
    recent_crops = farmer.crops.order_by('-created_at')[:5]
    
    # Performance metrics
    avg_profit_margin = farmer.crops.aggregate(
        avg_margin=Avg('investment_cost')
    )['avg_margin'] or 0
    
    context = {
        'farmer': farmer,
        'total_crops': total_crops,
        'total_value': total_value,
        'upcoming_harvests': upcoming_harvests,
        'crop_by_season': crop_by_season,
        'crop_by_status': crop_by_status,
        'recent_crops': recent_crops,
        'avg_profit_margin': avg_profit_margin,
    }
    
    return render(request, 'kisan_app/farmer_detail.html', context)


def crops_list(request):
    """Enhanced crops list with filtering and sorting"""
    crops = Crop.objects.select_related('farmer', 'category').all()
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        crops = crops.filter(
            Q(name__icontains=search) |
            Q(farmer__name__icontains=search) |
            Q(season__icontains=search)
        )
    
    # Filter by season
    season = request.GET.get('season')
    if season:
        crops = crops.filter(season=season)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        crops = crops.filter(status=status)
    
    # Sort by
    sort_by = request.GET.get('sort', 'harvest_date')
    if sort_by == 'value':
        crops = sorted(crops, key=lambda x: x.total_value, reverse=True)
    elif sort_by == 'profit':
        crops = sorted(crops, key=lambda x: x.profit, reverse=True)
    else:
        crops = crops.order_by('harvest_date')
    
    # Get filter options
    seasons = Crop.SEASON_CHOICES
    statuses = Crop.STATUS_CHOICES
    
    context = {
        'crops': crops,
        'search': search,
        'season': season,
        'status': status,
        'sort_by': sort_by,
        'seasons': seasons,
        'statuses': statuses,
    }
    
    return render(request, 'kisan_app/crops_list.html', context)


def analytics_dashboard(request):
    """Advanced analytics dashboard"""
    # Overall statistics
    total_farmers = Farmer.objects.count()
    total_crops = Crop.objects.count()
    total_investment = Crop.objects.aggregate(Sum('investment_cost'))['investment_cost__sum'] or 0
    total_revenue = sum(crop.total_value for crop in Crop.objects.all())
    total_profit = sum(crop.profit for crop in Crop.objects.all())
    
    # Monthly data for charts
    from django.db.models.functions import TruncMonth
    monthly_data = Crop.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id'),
        revenue=Sum('quantity')
    ).order_by('month')
    
    # Crop distribution
    crop_distribution = Crop.objects.values('season').annotate(
        count=Count('id'),
        total_value=Sum('quantity')
    )
    
    # Top performing crops
    top_crops = Crop.objects.order_by('-quantity')[:5]
    
    # Upcoming harvests
    upcoming_harvests = Crop.objects.filter(
        harvest_date__gte=date.today(),
        harvest_date__lte=date.today() + timedelta(days=30)
    ).order_by('harvest_date')
    
    # Overdue crops
    overdue_crops = Crop.objects.filter(
        harvest_date__lt=date.today(),
        status__in=['Planted', 'Growing']
    )
    
    context = {
        'total_farmers': total_farmers,
        'total_crops': total_crops,
        'total_investment': total_investment,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'monthly_data': list(monthly_data),
        'crop_distribution': list(crop_distribution),
        'top_crops': top_crops,
        'upcoming_harvests': upcoming_harvests,
        'overdue_crops': overdue_crops,
    }
    
    return render(request, 'kisan_app/analytics_dashboard.html', context)


def price_calculator(request):
    """Crop price calculator with market comparison"""
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        quantity = float(request.POST.get('quantity', 0))
        your_price = float(request.POST.get('price', 0))
        
        # Get market prices
        market_prices = MarketPrice.objects.filter(
            crop_name__icontains=crop_name
        ).order_by('-date_recorded')[:5]
        
        # Calculate values
        your_total = quantity * your_price
        
        calculations = []
        for market_price in market_prices:
            market_total = quantity * market_price.price_per_kg
            difference = market_total - your_total
            percentage = (difference / your_total * 100) if your_total > 0 else 0
            
            calculations.append({
                'market': market_price.market_location,
                'price': market_price.price_per_kg,
                'total': market_total,
                'difference': difference,
                'percentage': percentage,
                'date': market_price.date_recorded
            })
        
        return JsonResponse({
            'your_total': your_total,
            'calculations': calculations
        })
    
    # Get recent market prices for display
    recent_prices = MarketPrice.objects.order_by('-date_recorded')[:10]
    
    context = {
        'recent_prices': recent_prices
    }
    
    return render(request, 'kisan_app/price_calculator.html', context)


def weather_info(request):
    """Weather information page"""
    # Get latest weather data
    weather_data = WeatherData.objects.order_by('-date_recorded')[:10]
    
    # Get unique locations
    locations = WeatherData.objects.values_list('location', flat=True).distinct()
    
    context = {
        'weather_data': weather_data,
        'locations': locations,
    }
    
    return render(request, 'kisan_app/weather_info.html', context)


def notifications_view(request):
    """User notifications"""
    # For now, show all notifications (in real app, filter by user)
    notifications = Notification.objects.order_by('-created_at')[:20]
    
    # Mark as read if requested
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        if notification_id:
            Notification.objects.filter(id=notification_id).update(is_read=True)
            return JsonResponse({'status': 'success'})
    
    context = {
        'notifications': notifications
    }
    
    return render(request, 'kisan_app/notifications.html', context)