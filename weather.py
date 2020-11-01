import requests
import json
import datetime as dt
import pytz
from pytz import timezone

class Weather:

    def __init__(self):
        self.mapquest_key, self.weather_key, self.zipcode = self.config()
        self.city, self.county, self.latitude, self.longitude = self.get_lat_lng_coords()
        self.weather = self.get_weather()
        self.tz = timezone('US/Pacific')
        self.time_fmt = '%I:%M %p'

    def config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            mapquest_key = config["MAPQUEST_KEY"]
            weather_key = config["OPENWEATHER_KEY"]
            zipcode = config["ZIPCODE"]
        
        return mapquest_key, weather_key, zipcode

    def get_lat_lng_coords(self):
        url = f'http://www.mapquestapi.com/geocoding/v1/address?key={self.mapquest_key}&postalCode={self.zipcode}'
        res = requests.get(url).json()["results"][0]["locations"][0]
        city = res["adminArea5"]
        county = res["adminArea4"]
        lat = res["latLng"]["lat"]
        lng = res["latLng"]["lng"]
        return city, county, lat, lng

    def get_weather(self):
        base = 'https://api.openweathermap.org/data/2.5/onecall?'
        params = f'lat={self.latitude}&lon={self.longitude}&exclude=minutely&units=imperial&appid={self.weather_key}'
        url = base + params
        weather = requests.get(url).json()
        return weather

    def today(self):
        end_time = dt.datetime.today().astimezone(self.tz).replace(hour=23, minute=59, second=59)
        cur_time = dt.datetime.now().astimezone(self.tz)
        remaining_hrs = (end_time - cur_time).seconds // 3600 + 2 # add 1 to round up, add another for midnight
        
        # hourly = self.weather["hourly"][1:remaining_hrs + 1]
        cur_day = self.weather["daily"][0]

        sunrise = dt.datetime.fromtimestamp(cur_day["sunrise"], pytz.UTC).astimezone(self.tz).strftime(self.time_fmt)
        sunset = dt.datetime.fromtimestamp(cur_day["sunset"], pytz.UTC).astimezone(self.tz).strftime(self.time_fmt)
        wind = cur_day["wind_speed"]
        weather_desc = cur_day["weather"][0]["description"]
        chance_of_rain = "{:.0%}".format(cur_day["pop"])
        morn = cur_day["temp"]["morn"]
        midday = cur_day["temp"]["day"]
        night = cur_day["temp"]["night"]
        dt_today = dt.datetime.fromtimestamp(cur_day["dt"], pytz.UTC).astimezone(self.tz).strftime('%b %d, %Y')
        cloudiness = "{:.0%}".format(cur_day["clouds"] / 100)

        msg = (
            f"-> It is: {dt_today}, {cur_time.strftime(self.time_fmt)} <-\n"
            "-----\n"
            f"Morning: {morn} degrees\n"
            f"Midday: {midday} degrees\n"
            f"Night: {night} degrees\n"
            "-----\n"
            f"Chance of Rain: {chance_of_rain}\n"
            f"Cloudiness: {cloudiness}\n"
            f"Wind Levels: {wind} miles/hour\n"
            f"Weather Description: {weather_desc}\n"
            "-----\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}\n"
            "\n"
        )
        print(msg)
    
    def forecast(self, days=1):
        print(f"######### {days} DAY FORECAST ############")
        forecast = self.weather["daily"]
        for day in forecast[1:days+1]:
            daily_info = {
                "future_date": dt.datetime.fromtimestamp(day['dt'], pytz.UTC).astimezone(self.tz).strftime('%b %d, %Y'),
                "high": day["temp"]["max"],
                "low": day["temp"]["min"],
                "rain": "{:.0%}".format(day["pop"]),
                "sunrise": dt.datetime.fromtimestamp(day["sunrise"], pytz.UTC).astimezone(self.tz).strftime(self.time_fmt),
                "sunset": dt.datetime.fromtimestamp(day["sunset"], pytz.UTC).astimezone(self.tz).strftime(self.time_fmt)
            }
        
            forecast_msg = (
                "\n"
                f"-> {daily_info['future_date']}:\n"
                f"High: {daily_info['high']} degrees\n"
                f"Low: {daily_info['low']} degrees\n"
                f"Chance of Rain: {daily_info['rain']}\n"
                "-----\n"
                f"Sunrise: {daily_info['sunrise']}\n"
                f"Sunset: {daily_info['sunset']}\n"
            )
            print(forecast_msg)
            input("Press enter to continue\n")

    def display_weather(self):
        print(f"\nGood morning in: \n\n-> {self.city} | {self.county} <-")
        input("\nPress Enter to continue to today's weather\n")
        self.today()
        input("Press Enter to continue to forecast\n")
        self.forecast(1)
        print("\nHAVE A NICE DAY!\n")

if __name__=='__main__':
    weather = Weather()
    weather.display_weather()
