import os
import requests

WEATHER_TOKEN = os.environ.get('WEATHER_TOKEN')


WEATHER_MSG = """
*{city}*
_{conditions}_
Temperature: _{temp} C_
Humidity: _{humidity} %_
Pressure: _{pressure} hPa_
Wind speed: _{windspeed} m/s_
"""

__all__ = ['OpenWeatherMapApi']


class OpenWeatherMapApi(object):

    def data(self, **kwargs):
        data = {
            'APPID': WEATHER_TOKEN,
            'units': 'metric',
            'lang': 'en',
        }
        data.update(**kwargs)
        return data

    def format_city(self, data):
        text = WEATHER_MSG.format(
            city=data['name'],
            conditions=data['weather'][0]['description'],
            temp=data['main']['temp'],
            temp_min=data['main']['temp_min'],
            temp_max=data['main']['temp_max'],
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            windspeed=data['wind']['speed'],
        )
        return text

    def get_city_message(self, city):
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather', params=self.data(q=city))

        if response.status_code == 200:
            data = response.json()
            return self.format_city(data)

    def get_default_cities(self):
        ids = ['520555', '1496747', '709930']
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/group', params=self.data(id=','.join(ids)))
        if response.status_code == 200:
            result = ""
            for data in response.json()['list']:
                text = self.format_city(data)
                result += '\n' + text
            return result
