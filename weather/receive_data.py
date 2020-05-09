import requests as rq
import json

from config import weather_api_call, json_weather_path


#  Получение данных (погоды) с сайта и сохранение в json
class ReceiveWeather:

    @staticmethod
    def start(w_type):
        resp = rq.get(weather_api_call.format(w_type))
        info = resp.json()
        f = open("{0}{1}.json".format(json_weather_path, w_type), "w")
        save = json.dumps(info, ensure_ascii=False, indent=4)
        f.write(save)
        f.close()
