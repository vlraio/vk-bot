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
        response = "Погода в Москве сейчас.@"

        img = None

        for key, value in Weather.get_data("weather").items():

            if key == "weather":
                img = "{0}{1}.png".format(icons_path, value[0]["icon"])
                response += "{}, ".format(value[0]["description"].capitalize())

            if key == "main":
                response += "температура: {0} - {1}°C\n".format(round(value["temp_min"]), round(value["temp_max"]))
                response += "Давление: {} мм. рт. ст., ".format(int(value["pressure"] * 0.75))
                response += "влажность: {}%\n".format(value["humidity"])

            if key == "wind":
                response += Weather.wind(round(value["speed"]), value["deg"])

        return response, img

    @staticmethod
    def get_weather_today():
        title = "Погода в Москве на день.@"
        sub_title = ""
        big_resp = ""
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
                        big_resp += time[0]
                    elif hour == 6 or hour == 3:
                        big_resp += time[1]
                    elif hour == 12 or hour == 9:
                        big_resp += time[2]
                    elif hour == 18 or hour == 15:
                        big_resp += time[3]

                    minimum, maximum, t = Weather.text(value[i], value[i + 1])
                    big_resp += t

                    sub_title += "/ {}°C /".format(int((minimum + maximum) // 2))

                    img.append("{0}{1}.png".format(icons_path, value[i]["weather"][0]["icon"]))
                break

        r, img = Weather.save(sub_title, big_resp, img)
        title += r

        return title, img

    @staticmethod
    def get_weather_tomorrow(day, five: bool = False):
        title = "Погода в Москве на завтра.@"
        sub_title = ""
        big_resp = ""
        img = []
        time = ["\nНОЧЬ\n", "\nУТРО\n", "\nДЕНЬ\n", "\nВЕЧЕР\n"]

        mid_day = ""
        night = ""
        mid_day_img = ""

        for key, value in Weather.get_data("forecast").items():
            if key == "list":
                i = 0
                first_half = [0, 1, 2, 6, 7, 8, 12, 13, 14, 18, 19, 20]
                f = 0
                if day.hour not in first_half:
                    f = 1

                for v in range(f, len(value), 2):
                    op = value[v]
                    if str(day.date()) == op["dt_txt"].split()[0]:
                        img.append("{0}{1}.png".format(icons_path, op["weather"][0]["icon"]))

                        big_resp += time[i]

                        minimum, maximum, t = Weather.text(op, value[v+1])
                        big_resp += t

                        if five and (i == 0 or i == 2):
                            if i == 2:
                                mid_day = int(maximum)
                                mid_day_img = "{0}{1}.png".format(icons_path, op["weather"][0]["icon"])
                            else:
                                night = int(minimum)

                        elif not five:
                            sub_title += "/ {}°C /".format(int((minimum + maximum) // 2))

                        i += 1

        if five:
            return mid_day, night, mid_day_img

        r, img = Weather.save(sub_title, big_resp, img)
        title += r

        return title, img

    @staticmethod
    def get_weather_5_days(first):
        last = first + timedelta(days=5)
        response = "Погода в Москве с {0} по {1}.@".format(first.date().strftime("%d.%m"),
                                                           last.date().strftime("%d.%m"))

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
                d = 15
            response += "/ {}°C /".format(d)
        response += " ДЕНЬ\n"
        for n in night:
            if n == "":
                response += "/ ---- /"
            else:
                if n > 10:
                    n = 4
                response += "/ {}°C /".format(n)
        response += " НОЧЬ\n"

        new_image = Image.new("RGBA", (250, 50))
        c = 0
        for i in img:
            if i == "":
                i = "{}10d.png".format(icons_path)
            img2 = Image.open(i)
            new_image.paste(img2, (c, 0))
            c += 50

        new_image.save("{}temp/new.png".format(icons_path))

        return response, "{}temp/new.png".format(icons_path)

    @staticmethod
    def text(p1, p2):
        min_ = round(min(p1["main"]["temp_min"], p2["main"]["temp_min"]), 1)
        max_ = round(max(p1["main"]["temp_max"], p2["main"]["temp_max"]), 1)

        txt = "// {}, ".format(p1["weather"][0]["description"].capitalize())
        txt += "температура: {0} - {1}°C\n".format(min_, max_)
        txt += "// Давление: {} мм. рт. ст., ".format(int(p1["main"]["pressure"] * 0.75))
        txt += "влажность: {}%\n".format(p1["main"]["humidity"])
        txt += "// {}".format(Weather.wind(p1["wind"]["speed"], p1["wind"]["deg"]))

        return min_, max_, txt


    @staticmethod
    def wind(speed, degrees):
        res = ""
        for k, v in wind_beaufort_dict.items():
            if v[0] <= speed <= v[1]:
                res += "Ветер: {0}, {1} м/с, ".format(k, round(speed))
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

