import json

from config import json_weather_path


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

        for key, value in Weather.get_data("weather").items():
            if key == "weather":
                response += "{}, ".format(value[0]["description"])
            if key == "main":
                response += "{0}-{1}\n".format(value["temp_min"], value["temp_max"])
                response += "Давление: {}, ".format(value["pressure"])
                response += "влажность: {}%\n".format(value["humidity"])
            if key == "wind":
                response += "Ветер: {} м/с\n".format(value["speed"])
        return response
