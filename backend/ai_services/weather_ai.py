"""
Weather AI Service - Real-time weather prediction and analysis
Uses multiple weather APIs for comprehensive forecasting
"""

import os
import asyncio
import aiohttp
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger()

class WeatherAI:
    """Advanced weather prediction service using multiple APIs"""
    
    def __init__(self):
        self.openweather_key = os.getenv('OPENWEATHER_API_KEY')
        self.tomorrow_key = os.getenv('TOMORROW_API_KEY')
        self.climatic_key = os.getenv('CLIMATIC_API_KEY')
        self.airvisual_key = os.getenv('AIRVISUAL_API_KEY')
        
        # API endpoints
        self.openweather_base = "https://api.openweathermap.org/data/2.5"
        self.tomorrow_base = "https://api.tomorrow.io/v4"
        self.airvisual_base = "https://api.airvisual.com/v2"
        self.usgs_earthquake = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary"
        
        # Weather severity thresholds
        self.severity_thresholds = {
            'temperature': {'extreme_hot': 40, 'hot': 35, 'cold': -10, 'extreme_cold': -20},
            'wind_speed': {'high': 15, 'extreme': 25},  # m/s
            'precipitation': {'heavy': 10, 'extreme': 25},  # mm/hour
            'humidity': {'high': 80, 'low': 20},
            'pressure': {'low': 1000, 'high': 1030}  # hPa
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _make_request(self, url: str, params: Dict = None, timeout: int = 30) -> Dict:
        """Make HTTP request with retry logic"""
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("API request failed", url=url, error=str(e))
            raise

    def get_coordinates(self, location: str) -> tuple:
        """Get latitude and longitude for a location"""
        try:
            if not self.openweather_key:
                raise ValueError("OpenWeather API key not configured")
                
            url = f"{self.openweather_base}/weather"
            params = {
                'q': location,
                'appid': self.openweather_key
            }
            
            data = self._make_request(url, params)
            return data['coord']['lat'], data['coord']['lon']
            
        except Exception as e:
            logger.error("Failed to get coordinates", location=location, error=str(e))
            # Default to New York coordinates if geocoding fails
            return 40.7128, -74.0060

    def get_current_weather(self, location: str) -> Dict:
        """Get current weather conditions"""
        try:
            if not self.openweather_key:
                return self._get_fallback_weather(location)
                
            url = f"{self.openweather_base}/weather"
            params = {
                'q': location,
                'appid': self.openweather_key,
                'units': 'metric'
            }
            
            data = self._make_request(url, params)
            
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 10000) / 1000,  # Convert to km
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'clouds': data['clouds']['all'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat(),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Failed to get current weather", location=location, error=str(e))
            return self._get_fallback_weather(location)

    def get_forecast(self, location: str, days: int = 7) -> List[Dict]:
        """Get weather forecast"""
        try:
            if not self.openweather_key:
                return self._get_fallback_forecast(location, days)
                
            url = f"{self.openweather_base}/forecast"
            params = {
                'q': location,
                'appid': self.openweather_key,
                'units': 'metric',
                'cnt': min(days * 8, 40)  # 3-hour intervals, max 5 days
            }
            
            data = self._make_request(url, params)
            
            forecast = []
            for item in data['list']:
                forecast.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'wind_speed': item['wind']['speed'],
                    'wind_direction': item['wind'].get('deg', 0),
                    'weather_main': item['weather'][0]['main'],
                    'weather_description': item['weather'][0]['description'],
                    'clouds': item['clouds']['all'],
                    'precipitation': item.get('rain', {}).get('3h', 0) + item.get('snow', {}).get('3h', 0)
                })
            
            return forecast
            
        except Exception as e:
            logger.error("Failed to get forecast", location=location, error=str(e))
            return self._get_fallback_forecast(location, days)

    def get_air_quality(self, location: str) -> Dict:
        """Get air quality data"""
        try:
            lat, lon = self.get_coordinates(location)
            
            # Try AirVisual API first
            if self.airvisual_key:
                try:
                    url = f"{self.airvisual_base}/nearest_city"
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'key': self.airvisual_key
                    }
                    
                    data = self._make_request(url, params)
                    pollution = data['data']['current']['pollution']
                    
                    return {
                        'aqi': pollution['aqius'],
                        'main_pollutant': pollution['mainus'],
                        'pm2_5': pollution.get('pm25', 0),
                        'pm10': pollution.get('pm10', 0),
                        'o3': pollution.get('o3', 0),
                        'no2': pollution.get('no2', 0),
                        'so2': pollution.get('so2', 0),
                        'co': pollution.get('co', 0),
                        'timestamp': datetime.utcnow().isoformat(),
                        'source': 'AirVisual'
                    }
                except Exception as e:
                    logger.warning("AirVisual API failed", error=str(e))
            
            # Fallback to OpenWeather Air Pollution API
            if self.openweather_key:
                try:
                    url = f"{self.openweather_base}/air_pollution"
                    params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': self.openweather_key
                    }
                    
                    data = self._make_request(url, params)
                    components = data['list'][0]['components']
                    
                    return {
                        'aqi': data['list'][0]['main']['aqi'],
                        'pm2_5': components.get('pm2_5', 0),
                        'pm10': components.get('pm10', 0),
                        'o3': components.get('o3', 0),
                        'no2': components.get('no2', 0),
                        'so2': components.get('so2', 0),
                        'co': components.get('co', 0),
                        'timestamp': datetime.utcnow().isoformat(),
                        'source': 'OpenWeather'
                    }
                except Exception as e:
                    logger.warning("OpenWeather air pollution API failed", error=str(e))
            
            # Return fallback data
            return self._get_fallback_air_quality()
            
        except Exception as e:
            logger.error("Failed to get air quality", location=location, error=str(e))
            return self._get_fallback_air_quality()

    def get_earthquake_data(self, location: str) -> List[Dict]:
        """Get recent earthquake data"""
        try:
            lat, lon = self.get_coordinates(location)
            
            # Get significant earthquakes from the past week
            url = f"{self.usgs_earthquake}/significant_week.geojson"
            data = self._make_request(url)
            
            earthquakes = []
            for feature in data['features'][:10]:  # Limit to 10 most recent
                props = feature['properties']
                coords = feature['geometry']['coordinates']
                
                # Calculate distance from location (rough approximation)
                eq_lat, eq_lon = coords[1], coords[0]
                distance = ((lat - eq_lat) ** 2 + (lon - eq_lon) ** 2) ** 0.5 * 111  # Rough km conversion
                
                earthquakes.append({
                    'magnitude': props['mag'],
                    'location': props['place'],
                    'time': datetime.fromtimestamp(props['time'] / 1000).isoformat(),
                    'depth': coords[2],
                    'latitude': eq_lat,
                    'longitude': eq_lon,
                    'distance_km': round(distance, 1),
                    'url': props['url']
                })
            
            # Sort by distance
            earthquakes.sort(key=lambda x: x['distance_km'])
            
            return earthquakes
            
        except Exception as e:
            logger.error("Failed to get earthquake data", error=str(e))
            return []

    def analyze_weather_risks(self, current_weather: Dict, forecast: List[Dict]) -> Dict:
        """Analyze weather risks and generate alerts"""
        risks = []
        risk_level = "low"
        
        try:
            # Current weather risks
            temp = current_weather.get('temperature', 20)
            wind_speed = current_weather.get('wind_speed', 0)
            humidity = current_weather.get('humidity', 50)
            
            # Temperature risks
            if temp >= self.severity_thresholds['temperature']['extreme_hot']:
                risks.append({
                    'type': 'extreme_heat',
                    'severity': 'critical',
                    'message': f'Extreme heat warning: {temp}°C',
                    'recommendations': ['Stay indoors', 'Drink plenty of water', 'Avoid outdoor activities']
                })
                risk_level = "critical"
            elif temp >= self.severity_thresholds['temperature']['hot']:
                risks.append({
                    'type': 'high_temperature',
                    'severity': 'high',
                    'message': f'High temperature alert: {temp}°C',
                    'recommendations': ['Limit outdoor exposure', 'Stay hydrated']
                })
                if risk_level == "low":
                    risk_level = "high"
            
            # Wind risks
            if wind_speed >= self.severity_thresholds['wind_speed']['extreme']:
                risks.append({
                    'type': 'extreme_wind',
                    'severity': 'critical',
                    'message': f'Extreme wind warning: {wind_speed} m/s',
                    'recommendations': ['Avoid travel', 'Secure loose objects', 'Stay indoors']
                })
                risk_level = "critical"
            elif wind_speed >= self.severity_thresholds['wind_speed']['high']:
                risks.append({
                    'type': 'high_wind',
                    'severity': 'moderate',
                    'message': f'High wind alert: {wind_speed} m/s',
                    'recommendations': ['Exercise caution outdoors', 'Secure loose items']
                })
                if risk_level == "low":
                    risk_level = "moderate"
            
            # Forecast risks
            for day in forecast[:3]:  # Check next 3 days
                precip = day.get('precipitation', 0)
                if precip >= self.severity_thresholds['precipitation']['extreme']:
                    risks.append({
                        'type': 'heavy_precipitation',
                        'severity': 'high',
                        'message': f'Heavy precipitation expected: {precip}mm',
                        'date': day.get('datetime', ''),
                        'recommendations': ['Avoid flood-prone areas', 'Plan indoor activities']
                    })
                    if risk_level in ["low", "moderate"]:
                        risk_level = "high"
            
            return {
                'risk_level': risk_level,
                'risks': risks,
                'total_risks': len(risks),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Weather risk analysis failed", error=str(e))
            return {
                'risk_level': 'unknown',
                'risks': [],
                'total_risks': 0,
                'error': str(e)
            }

    def get_predictions(self, location: str, range_days: str = "7d") -> Dict:
        """Get comprehensive weather predictions"""
        try:
            days = int(range_days.replace('d', ''))
            
            logger.info("Getting weather predictions", location=location, days=days)
            
            # Get current weather and forecast
            current_weather = self.get_current_weather(location)
            forecast = self.get_forecast(location, days)
            air_quality = self.get_air_quality(location)
            earthquakes = self.get_earthquake_data(location)
            
            # Analyze risks
            risk_analysis = self.analyze_weather_risks(current_weather, forecast)
            
            return {
                'location': location,
                'current_weather': current_weather,
                'forecast': forecast,
                'air_quality': air_quality,
                'earthquakes': earthquakes,
                'risk_analysis': risk_analysis,
                'risk_level': risk_analysis['risk_level'],
                'data_sources': ['OpenWeather', 'AirVisual', 'USGS'],
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Weather predictions failed", location=location, error=str(e))
            return {
                'location': location,
                'error': str(e),
                'fallback_data': self._get_fallback_predictions(location),
                'timestamp': datetime.utcnow().isoformat()
            }

    def get_alerts(self, location: str) -> Dict:
        """Get current weather alerts"""
        try:
            current_weather = self.get_current_weather(location)
            air_quality = self.get_air_quality(location)
            
            alerts = []
            
            # Temperature alerts
            temp = current_weather.get('temperature', 20)
            if temp >= 35:
                alerts.append({
                    'type': 'heat_warning',
                    'severity': 'high',
                    'message': f'Heat warning: {temp}°C',
                    'issued': datetime.utcnow().isoformat()
                })
            
            # Air quality alerts
            aqi = air_quality.get('aqi', 1)
            if aqi >= 150:  # Unhealthy
                alerts.append({
                    'type': 'air_quality',
                    'severity': 'high',
                    'message': f'Poor air quality: AQI {aqi}',
                    'issued': datetime.utcnow().isoformat()
                })
            
            return {
                'location': location,
                'alerts': alerts,
                'alert_count': len(alerts),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error("Weather alerts failed", location=location, error=str(e))
            return {
                'location': location,
                'alerts': [],
                'alert_count': 0,
                'error': str(e)
            }

    def _get_fallback_weather(self, location: str) -> Dict:
        """Fallback weather data when APIs fail"""
        return {
            'temperature': 22,
            'feels_like': 24,
            'humidity': 65,
            'pressure': 1013,
            'wind_speed': 3.5,
            'wind_direction': 180,
            'visibility': 10,
            'weather_main': 'Clear',
            'weather_description': 'clear sky',
            'clouds': 20,
            'sunrise': (datetime.utcnow() + timedelta(hours=6)).isoformat(),
            'sunset': (datetime.utcnow() + timedelta(hours=18)).isoformat(),
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'fallback',
            'warning': 'Using fallback data - API unavailable'
        }

    def _get_fallback_forecast(self, location: str, days: int) -> List[Dict]:
        """Fallback forecast data"""
        forecast = []
        base_temp = 22
        
        for i in range(days * 4):  # 6-hour intervals
            forecast.append({
                'datetime': (datetime.utcnow() + timedelta(hours=i * 6)).isoformat(),
                'temperature': base_temp + (i % 3) - 1,
                'feels_like': base_temp + (i % 3),
                'humidity': 60 + (i % 20),
                'pressure': 1013 + (i % 10) - 5,
                'wind_speed': 3 + (i % 5),
                'wind_direction': (i * 45) % 360,
                'weather_main': 'Clear',
                'weather_description': 'clear sky',
                'clouds': 20 + (i % 30),
                'precipitation': 0,
                'source': 'fallback'
            })
        
        return forecast

    def _get_fallback_air_quality(self) -> Dict:
        """Fallback air quality data"""
        return {
            'aqi': 50,
            'main_pollutant': 'pm2_5',
            'pm2_5': 12,
            'pm10': 20,
            'o3': 80,
            'no2': 25,
            'so2': 5,
            'co': 0.3,
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'fallback',
            'warning': 'Using fallback data - API unavailable'
        }

    def _get_fallback_predictions(self, location: str) -> Dict:
        """Fallback predictions when all APIs fail"""
        return {
            'current_weather': self._get_fallback_weather(location),
            'forecast': self._get_fallback_forecast(location, 7),
            'air_quality': self._get_fallback_air_quality(),
            'earthquakes': [],
            'risk_analysis': {
                'risk_level': 'low',
                'risks': [],
                'total_risks': 0
            },
            'warning': 'Using fallback data - APIs unavailable'
        }
