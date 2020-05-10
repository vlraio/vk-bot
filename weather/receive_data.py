import requests as rq
import json

from config import weather_api_call, weather_link_png, json_weather_path, icons_path


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

    @staticmethod
    def load_icons():
        var = ["01{}", "02{}", "03{}", "04{}", "09{}", "10{}", "11{}", "13{}", "50{}"]
        mode = ["d", "n"]
        for m in mode:
            for v in var:
                resp = rq.get(weather_link_png.format(v.format(m)))
                with open("{0}{1}.png".format(icons_path, v.format(m)), "wb") as f:
                    f.write(resp.content)
                    f.close()
