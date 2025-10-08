from django.urls import path
from . import views

app_name = 'kisan_app'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('farmers/', views.farmers_list, name='farmers_list'),
    path('farmer/<int:farmer_id>/', views.farmer_detail, name='farmer_detail'),
    path('crops/', views.crops_list, name='crops_list'),
    
    # Advanced features
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('calculator/', views.price_calculator, name='price_calculator'),
    path('weather/', views.weather_info, name='weather_info'),
    path('notifications/', views.notifications_view, name='notifications'),
]