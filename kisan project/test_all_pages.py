"""
Test script to verify all Django application pages are working correctly
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kisan_project.settings')
django.setup()

def test_all_pages():
    """Test all major pages of the application"""
    client = Client()
    
    test_results = []
    
    # Test pages with their expected status codes
    pages_to_test = [
        ('kisan_app:home', 200, 'Home Page'),
        ('kisan_app:farmers_list', 200, 'Farmers List'),
        ('kisan_app:crops_list', 200, 'Crops List'),
        ('kisan_app:weather_info', 200, 'Weather Info'),
        ('kisan_app:analytics_dashboard', 200, 'Analytics Dashboard'),
        ('kisan_app:price_calculator', 200, 'Price Calculator'),
        ('kisan_app:notifications', 200, 'Notifications'),
    ]
    
    print("🧪 Testing all application pages...")
    print("=" * 50)
    
    for url_name, expected_status, page_name in pages_to_test:
        try:
            url = reverse(url_name)
            response = client.get(url)
            
            if response.status_code == expected_status:
                status = "✅ PASS"
                test_results.append(True)
            else:
                status = f"❌ FAIL (Status: {response.status_code})"
                test_results.append(False)
                
            print(f"{page_name:<20} | {url:<20} | {status}")
            
        except Exception as e:
            print(f"{page_name:<20} | {url_name:<20} | ❌ ERROR: {str(e)}")
            test_results.append(False)
    
    print("=" * 50)
    
    # Summary
    passed = sum(test_results)
    total = len(test_results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"📊 Test Summary:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 All pages are working correctly!")
        return True
    else:
        print("⚠️  Some pages have issues that need to be fixed.")
        return False

if __name__ == "__main__":
    success = test_all_pages()
    sys.exit(0 if success else 1)