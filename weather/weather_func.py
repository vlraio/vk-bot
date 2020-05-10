import json

from config import json_weather_path, json_icons_path, wind_beaufort_dict, wind_rumb_dict

#  Обработка запросов по погоде
class Weather:

    @staticmethod
    def get_data(w_type):
        with open("{0}{1}.json".format(json_weather_path, w_type), "r", encoding="UTF-8") as f:
            text = json.load(f)
            return text

    @staticmethod
    def get_weather_today():
        response = "\nПогода в Москве\n"
        icon = ""

        for key, value in Weather.get_data("weather").items():
            if key == "weather":
                response += "{}, ".format(value[0]["description"].title())
                icon = value[0]["icon"]

            if key == "main":
                response += "температура: {0} - {1}°C\n".format(value["temp_min"], value["temp_max"])
                response += "Давление: {} мм. рт. ст., ".format(int(value["pressure"] * 0.75))
                response += "влажность: {}%\n".format(value["humidity"])
            if key == "wind":
                speed = value["speed"]
                for k, v in wind_beaufort_dict.items():
                    if v[0] < speed < v[1]:
                        response += "Ветер: {0}, {1} м/с, ".format(k, speed)
                        break
                degrees = value["deg"]
                for k, v in wind_rumb_dict.items():
                    if v[0] < degrees < v[1]:
                        response += k
                        break
        return response, icon
