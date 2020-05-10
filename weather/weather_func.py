import json
import PIL.Image as Image
from datetime import timedelta
import re

from config import json_weather_path, icons_path, wind_beaufort_dict, wind_rumb_dict


#  Обработка запросов по погоде
class Weather:

    @staticmethod
    def get_data(w_type):
        with open("{0}{1}.json".format(json_weather_path, w_type), "r", encoding="UTF-8") as f:
            text = json.load(f)
            return text

    @staticmethod
    def get_weather_now():
        response = "\nПогода в Москве\n"
        img = None

        for key, value in Weather.get_data("weather").items():

            if key == "weather":
                img = "{0}{1}.png".format(icons_path, value[0]["icon"])
                response += "{}, ".format(value[0]["description"].capitalize())

            if key == "main":
                response += "температура: {0} - {1}°C\n".format(value["temp_min"], value["temp_max"])
                response += "Давление: {} мм. рт. ст., ".format(int(value["pressure"] * 0.75))
                response += "влажность: {}%\n".format(value["humidity"])

            if key == "wind":
                response += Weather.wind(value["speed"], value["deg"])

        return response, img

    @staticmethod
    def get_weather_today():
        res = "Погода в Москве на день.\n"
        response = ""
        img = []
        time = ["\nНОЧЬ\n", "\nУТРО\n", "\nДЕНЬ\n", "\nВЕЧЕР\n"]

        for key, value in Weather.get_data("forecast").items():
            if key == "list":
                hour = int(re.findall(r"\d{2}", value[0]["dt_txt"].split()[1])[0])
                start = 0

                if hour == 3 or hour == 9 or hour == 15 or hour == 21:
                    start = 1

                for i in range(start, 8 + start, 2):
                    hour = int(re.findall(r"\d{2}", value[i]["dt_txt"].split()[1])[0])

                    if hour == 0 or hour == 21:
                        response += time[0]
                    elif hour == 6 or hour == 3:
                        response += time[1]
                    elif hour == 12 or hour == 9:
                        response += time[2]
                    elif hour == 18 or hour == 15:
                        response += time[3]

                    minimum = min(value[i]["main"]["temp_min"], value[i]["main"]["temp_max"],
                                  value[i+1]["main"]["temp_min"], value[i+1]["main"]["temp_max"])
                    maximum = max(value[i]["main"]["temp_min"], value[i]["main"]["temp_max"],
                                  value[i+1]["main"]["temp_min"], value[i+1]["main"]["temp_max"])

                    res += "/ {}°C /".format(int((minimum + maximum) // 2))
                    if hour == 0:
                        img.append("{0}{1}.png".format(icons_path, value[i+1]["weather"][0]["icon"]))
                    else:
                        img.append("{0}{1}.png".format(icons_path, value[i]["weather"][0]["icon"]))

                    response += "// {}, ".format(value[i]["weather"][0]["description"].capitalize())

                    response += "температура: {0} - {1}°C\n".format(minimum, maximum)
                    response += "// Давление: {} мм. рт. ст., ".format(int(value[i]["main"]["pressure"] * 0.75))
                    response += "влажность: {}%\n".format(value[i]["main"]["humidity"])

                    response += "// {}".format(Weather.wind(value[i]["wind"]["speed"], value[i]["wind"]["deg"]))
                break

        return Weather.save(res, response, img)

    @staticmethod
    def get_weather_tomorrow(day, five: bool = False):
        response = ""
        res = ""
        if not five:
            res = "Погода в Москве на завтра.\n"

        time = ["\nНОЧЬ\n", "\nУТРО\n", "\nДЕНЬ\n", "\nВЕЧЕР\n"]
        img = []

        mid_day = ""
        night = ""
        mid_day_img = ""

        for key, value in Weather.get_data("forecast").items():
            if key == "list":
                i = 0
                for v in range(0, len(value), 2):
                    op = value[v]
                    if str(day.date()) == op["dt_txt"].split()[0]:
                        img.append("{0}{1}.png".format(icons_path, op["weather"][0]["icon"]))

                        minimum = min(op["main"]["temp_min"], value[v+1]["main"]["temp_min"])
                        maximum = max(op["main"]["temp_max"], value[v+1]["main"]["temp_max"])

                        if five and (i == 0 or i == 2):
                            if i == 2:
                                mid_day = int(maximum)
                                mid_day_img = "{0}{1}.png".format(icons_path, op["weather"][0]["icon"])
                            else:
                                night = int(minimum)

                        elif not five:
                            res += "/ {}°C /".format(int((minimum + maximum) // 2))

                        response += time[i]
                        i += 1

                        response += "// {}, ".format(op["weather"][0]["description"].capitalize())

                        response += "температура: {0} - {1}°C\n".format(minimum, maximum)
                        response += "// Давление: {} мм. рт. ст., ".format(int(op["main"]["pressure"] * 0.75))
                        response += "влажность: {}%\n".format(op["main"]["humidity"])

                        response += "// {}".format(Weather.wind(op["wind"]["speed"], op["wind"]["deg"]))

        if five:
            return mid_day, night, mid_day_img

        return Weather.save(res, response, img)

    @staticmethod
    def get_weather_5_days(first):
        last = first + timedelta(days=5)
        response = "Погода в Москве с {0} по {1}.\n\n".format(first.date(), last.date())

        day = []
        night = []
        img = []

        for i in range(5):
            d, n, im = Weather.get_weather_tomorrow(first + timedelta(days=i), True)
            day.append(d)
            night.append(n)
            img.append(im)

        for d in day:
            if d == "":
                response += "/ ---- /"
            else:
                response += "/ {}°C /".format(d)
        response += " ДЕНЬ\n"
        for n in night:
            if n == "":
                response += "/ ---- /"
            else:
                response += "/ {}°C /".format(n)
        response += " НОЧЬ\n"

        new_image = Image.new("RGBA", (250, 50))
        c = 0
        for i in img:
            if i == "":
                i = "{}00d.png".format(icons_path)
            img2 = Image.open(i)
            new_image.paste(img2, (c, 0))
            c += 50
        new_image.save("{}temp/new.png".format(icons_path))
        return response, "{}temp/new.png".format(icons_path)

    @staticmethod
    def wind(speed, degrees):
        res = ""
        for k, v in wind_beaufort_dict.items():
            if v[0] <= speed <= v[1]:
                res += "Ветер: {0}, {1} м/с, ".format(k, speed)
                break

        for k, v in wind_rumb_dict.items():
            if v[0] <= degrees <= v[1]:
                res += k
                break
        return res

    @staticmethod
    def save(res, response, img):
        res += "\n{}".format(response)
        new_image = Image.new("RGBA", (200, 50))
        c = 0
        for i in img:
            img2 = Image.open(i)
            new_image.paste(img2, (c, 0))
            c += 50
        new_image.save("{}temp/new.png".format(icons_path))
        return res, "{}temp/new.png".format(icons_path)

