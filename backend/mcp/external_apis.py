import requests
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from .models import ContextData

logger = logging.getLogger(__name__)

class WeatherAPI:
    """Fetch live weather data for regions"""

    def __init__(self):
        # Using OpenWeatherMap API (free tier)
        self.api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self, city, country="Nigeria"):
        """Get current weather data for a city"""
        if not self.api_key:
            logger.warning("OpenWeather API key not configured")
            return None

        try:
            params = {
                'q': f"{city},{country}",
                'appid': self.api_key,
                'units': 'metric'
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'rainfall': data.get('rain', {}).get('1h', 0),  # rainfall in last hour
                'description': data['weather'][0]['description'],
                'source': 'OpenWeatherMap'
            }

        except Exception as e:
            logger.error(f"Error fetching weather data for {city}: {str(e)}")
            return None

class DiseaseAPI:
    """Fetch disease outbreak data"""

    def __init__(self):
        # Using WHO or CDC APIs (mock implementation)
        self.base_url = "https://disease.sh/v3/covid-19"  # Example API

    def get_disease_trends(self, region):
        """Get disease trend data for a region"""
        try:
            # This is a simplified implementation
            # In production, integrate with WHO, CDC, or local health ministry APIs

            # Mock data for demonstration
            return {
                'disease_name': 'COVID-19',
                'case_count': 150,  # Mock data
                'trend_direction': 'stable',
                'source': 'Mock Health API'
            }

        except Exception as e:
            logger.error(f"Error fetching disease data for {region}: {str(e)}")
            return None

class GPSService:
    """GPS and location services using free alternatives"""

    def __init__(self):
        # Using OpenStreetMap Nominatim (free, no API key needed)
        self.base_url = "https://nominatim.openstreetmap.org/search"
        # Google Maps Geocoding API (requires API key)
        self.google_api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
        self.google_base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_coordinates(self, address):
        """Get GPS coordinates for an address using Google Maps (preferred) or OpenStreetMap (fallback)"""
        # Try Google Maps first if API key is available
        if self.google_api_key:
            coords = self.get_google_coordinates(address)
            if coords:
                return coords

        # Fallback to OpenStreetMap
        return self.get_openstreetmap_coordinates(address)

    def get_google_coordinates(self, address):
        """Get GPS coordinates using Google Maps Geocoding API"""
        if not self.google_api_key:
            return None

        try:
            params = {
                'address': address,
                'key': self.google_api_key,
                'region': 'ng'  # Bias results towards Nigeria
            }

            response = requests.get(self.google_base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data['status'] == 'OK' and data['results']:
                location = data['results'][0]['geometry']['location']
                return {
                    'latitude': location['lat'],
                    'longitude': location['lng'],
                    'source': 'Google Maps Geocoding API'
                }

        except Exception as e:
            logger.error(f"Error fetching Google Maps coordinates for {address}: {str(e)}")
            return None

        return None

    def get_openstreetmap_coordinates(self, address):
        """Get GPS coordinates for an address using OpenStreetMap Nominatim"""
        try:
            params = {
                'q': address,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'ng'  # Focus on Nigeria
            }

            # Add user agent as required by Nominatim
            headers = {
                'User-Agent': 'MedVault-MCP/1.0 (Healthcare Resource Management)'
            }

            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data:
                return {
                    'latitude': float(data[0]['lat']),
                    'longitude': float(data[0]['lon']),
                    'source': 'OpenStreetMap Nominatim'
                }

        except Exception as e:
            logger.error(f"Error fetching OpenStreetMap coordinates for {address}: {str(e)}")
            return None

        return None

    def get_static_coordinates(self, city):
        """Fallback static coordinates for major Nigerian cities"""
        static_coords = {
            'lagos': {'lat': 6.5244, 'lng': 3.3792},
            'abuja': {'lat': 9.0765, 'lng': 7.3986},
            'kano': {'lat': 12.0022, 'lng': 8.5920},
            'ibadan': {'lat': 7.3775, 'lng': 3.9470},
            'port harcourt': {'lat': 4.8156, 'lng': 7.0498},
            'benin city': {'lat': 6.3392, 'lng': 5.6174},
            'maiduguri': {'lat': 11.8464, 'lng': 13.1603},
            'zaria': {'lat': 11.1113, 'lng': 7.7227},
            'ilorin': {'lat': 8.4966, 'lng': 4.5421},
            'jos': {'lat': 9.8965, 'lng': 8.8583}
        }

        city_lower = city.lower()
        if city_lower in static_coords:
            return {
                'latitude': static_coords[city_lower]['lat'],
                'longitude': static_coords[city_lower]['lng'],
                'source': 'Static Coordinates'
            }

        return None

class ExternalDataManager:
    """Manages external API data collection and storage"""

    def __init__(self):
        self.weather_api = WeatherAPI()
        self.disease_api = DiseaseAPI()
        self.gps_service = GPSService()

    def update_weather_data(self, region):
        """Update weather data for a region"""
        weather_data = self.weather_api.get_weather_data(region)

        if weather_data:
            # Create or update context data
            context, created = ContextData.objects.get_or_create(
                region=region,
                data_type='weather',
                effective_date=timezone.now(),
                defaults={
                    'temperature': weather_data['temperature'],
                    'humidity': weather_data['humidity'],
                    'rainfall': weather_data['rainfall'],
                    'confidence_score': 0.9,
                    'source': weather_data['source'],
                    'expiry_date': timezone.now() + timedelta(hours=3)  # Weather data expires in 3 hours
                }
            )

            if not created:
                # Update existing record
                context.temperature = weather_data['temperature']
                context.humidity = weather_data['humidity']
                context.rainfall = weather_data['rainfall']
                context.source = weather_data['source']
                context.expiry_date = timezone.now() + timedelta(hours=3)
                context.save()

            logger.info(f"Updated weather data for {region}")
            return True

        return False

    def update_disease_data(self, region):
        """Update disease trend data for a region"""
        disease_data = self.disease_api.get_disease_trends(region)

        if disease_data:
            context, created = ContextData.objects.get_or_create(
                region=region,
                data_type='disease_trend',
                disease_name=disease_data['disease_name'],
                effective_date=timezone.now(),
                defaults={
                    'case_count': disease_data['case_count'],
                    'trend_direction': disease_data['trend_direction'],
                    'confidence_score': 0.8,
                    'source': disease_data['source'],
                    'expiry_date': timezone.now() + timedelta(days=1)  # Disease data expires daily
                }
            )

            if not created:
                context.case_count = disease_data['case_count']
                context.trend_direction = disease_data['trend_direction']
                context.source = disease_data['source']
                context.expiry_date = timezone.now() + timedelta(days=1)
                context.save()

            logger.info(f"Updated disease data for {region}")
            return True

        return False

    def update_all_regions(self, regions=None):
        """Update external data for all regions"""
        if not regions:
            # Get all regions from existing data
            regions = ContextData.objects.values_list('region', flat=True).distinct()
            if not regions:
                regions = ['Lagos', 'Abuja', 'Kano']  # Default regions

        updated_count = 0

        for region in regions:
            # Update weather
            if self.update_weather_data(region):
                updated_count += 1

            # Update disease trends
            if self.update_disease_data(region):
                updated_count += 1

        logger.info(f"Updated external data for {len(regions)} regions, {updated_count} records created/updated")
        return updated_count

    def get_live_weather(self, region):
        """Get live weather data for immediate use"""
        return self.weather_api.get_weather_data(region)

    def get_live_coordinates(self, address):
        """Get live GPS coordinates for an address"""
        # Try OpenStreetMap first
        coords = self.gps_service.get_coordinates(address)
        if coords:
            return coords

        # Fallback to static coordinates for major cities
        city = address.split(',')[0].strip()  # Extract city name
        return self.gps_service.get_static_coordinates(city)
