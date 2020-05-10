import requests as rq
import json

from config import weather_api_call, weather_link_png, json_weather_path, json_icons_path


#  Получение данных (погоды) с сайта и сохранение в json
class ReceiveWeather:

    def __init__(self, title):
        self.icon_title = title

    @staticmethod
    def start(w_type):
        resp = rq.get(weather_api_call.format(w_type))
        info = resp.json()
        f = open("{0}{1}.json".format(json_weather_path, w_type), "w")
        save = json.dumps(info, ensure_ascii=False, indent=4)
        f.write(save)
        f.close()

    def get_icon(self):
        return rq.get(weather_link_png.format(self.icon_title), stream=True)
