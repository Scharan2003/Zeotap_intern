import requests
import json
import time
import datetime

class WeatherMonitor:
    def __init__(self, api_key, interval=300):
        self.api_key = api_key
        self.interval = interval
        self.locations = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
        self.daily_summaries = {}

    def get_weather_data(self):
        for location in self.locations:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}'
            response = requests.get(url)
            data = json.loads(response.text)
            print(f"Response for {location}: {data}")  # Print the API response
            yield data

    def process_data(self, data):
        # Check for error in the response
        if 'cod' in data and data['cod'] != 200:
            print(f"Error fetching data: {data.get('message', 'Unknown error')}")
            return ('Unknown', 'Error', None, None, None)

        # Process the weather data
        main = data['weather'][0]['main'] if 'weather' in data and data['weather'] else 'Unknown'
        temp = data['main']['temp'] - 273.15 if 'main' in data and 'temp' in data['main'] else None
        feels_like = data['main']['feels_like'] - 273.15 if 'main' in data and 'feels_like' in data['main'] else None
        dt = data['dt'] if 'dt' in data else None
        location = data['name'] if 'name' in data else 'Unknown'

        print(f"Processed data for {location}: {main}, {temp}, {feels_like}, {dt}")  # Print processed data
        return (location, main, temp, feels_like, dt)

    def run(self):
        print("Starting weather monitor...")
        while True:
            for data in self.get_weather_data():
                location, main, temp, feels_like, dt = self.process_data(data)

                # Store daily summary only if data is valid
                if temp is not None and dt is not None:
                    self.store_daily_summary(location, main, temp, feels_like, dt)

                self.check_alerts(location, main, temp)
            time.sleep(self.interval)

    def store_daily_summary(self, location, main, temp, feels_like, dt):
        date = datetime.datetime.utcfromtimestamp(dt).date()
        if date not in self.daily_summaries:
            self.daily_summaries[date] = {}
        self.daily_summaries[date][location] = {'main': main, 'temp': temp, 'feels_like': feels_like}

    def check_alerts(self, location, main, temp):
        # Implement alerting thresholds here
        if temp is not None and temp > 35:  # Example threshold
            print(f"Alert: High temperature in {location}: {temp:.2f}°C")

if __name__ == '__main__':
    api_key = '06276b4d09f0055fed5c76287f78849a'  # Replace with your actual API key
    monitor = WeatherMonitor(api_key)
    monitor.run()