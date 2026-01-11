from django.shortcuts import render
import requests

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        
        
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocode_params = {'name': city, 'count': 1}
        
        try:
            
            geocode_response = requests.get(geocode_url, params=geocode_params)
            geocode_data = geocode_response.json()
            
            if geocode_data.get('results'):
                
                location = geocode_data['results'][0]
                latitude = location['latitude']
                longitude = location['longitude']
                country = location.get('country', '')
                
              
                weather_url = "https://api.open-meteo.com/v1/forecast"
                weather_params = {
                    'latitude': latitude,
                    'longitude': longitude,
                    'current_weather': True
                }
                
                weather_response = requests.get(weather_url, params=weather_params)
                weather_data = weather_response.json()
                
                 
                current_weather = weather_data['current_weather']
                
                context = {
                    'weather_data': current_weather,
                    'city': city,
                    'country': country
                }
                
                return render(request, 'index.html', context)
            else:
                return render(request, 'index.html', {'error': f"City '{city}' not found"})
                
        except Exception as e:
            return render(request, 'index.html', {'error': f"Error: {str(e)}"})
    
     
    return render(request, 'index.html')