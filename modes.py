from datetime import datetime, timedelta
import locale
import re

from schedule.schedule_func import Schedule
from weather.weather_func import Weather
from config import GROUP_REGEX, week_day_dict


class ModeWork:

    @staticmethod
    def schedule(message, group):
        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
        today = datetime.today()
        #  Номер группы
        if message == "Какая группа?":
            return "Вы обучаетесь в группе {}.".format(group), group

        #  Номер недели
        elif message == "Какая неделя?":
            return "Идет {} неделя.".format(Schedule.count_week_num()), group

        #  Расписание на сегодня
        elif message == "На сегодня":
            #  Определение четности/нечетности недели (0 - н/ч; 1 - ч)
            week_type = int(not Schedule.count_week_num() % 2)
            return Schedule.get_response_schedule(group, today, week_type, True), group

        #  Расписание на завтра
        elif message == "На завтра":
            week_type = int(not Schedule.count_week_num() % 2)
            tomorrow = today + timedelta(days=1)
            return Schedule.get_response_schedule(group, tomorrow, week_type, True), group

        #  Расписание на текущую неделю
        elif message == "На эту неделю":
            #  Первый день текущей недели
            start = today - timedelta(days=today.weekday())
            week_type = int(not Schedule.count_week_num() % 2)
            return Schedule.get_response_schedule(group, start, week_type), group

        #  Расписание на следующую неделю
        elif message == "На следующую неделю":
            start = today + timedelta(days=7) - timedelta(days=today.weekday())
            week_type = int(Schedule.count_week_num() % 2)
            return Schedule.get_response_schedule(group, start, week_type), group

        elif re.match(r"Бот [А-Я,а-я]+", message):
            mes = message.replace("Бот ", "").replace(" ", "-").split()

            #  Проверка на ввод "Бот <день_недели>"
            if mes[0].title() in week_day_dict.keys() != "-" and len(mes[0]) <= 11 and re.match(r"[а-я]{5,}", mes[0]):
                return Schedule.get_response_for_day_schedule(group, mes[0]), group

            #  Проверка на ввод "Бот <номер_группы>"
            elif re.match(GROUP_REGEX, mes[0]):
                group = mes[0].upper()
                return "Доступно расписание для группы {}.".format(group), group

            #  Проверка на ввод "Бот <день_недели номер_группы>"
            else:
                arr = mes[0].replace("-", " ", 1).split()
                if arr[0].title() in week_day_dict.keys() and re.match(r"[а-я]{5,}", arr[0]) and re.match(GROUP_REGEX,
                                                                                                          arr[1]):
                    return Schedule.get_response_for_day_schedule(arr[1].upper(), arr[0]), group

        return "Неверно введена команда.", group

    @staticmethod
    def weather(message):
        today = datetime.today()
        if message == "Сейчас":
            return Weather.get_weather_now()

        if message == "В течение дня":
            return Weather.get_weather_today()

        if message == "Завтра":
            tomorrow = today + timedelta(days=1)
            return Weather.get_weather_tomorrow(tomorrow)

        if message == "На 5 дней":
            return Weather.get_weather_5_days(today)

        return "Неверно введена команда."
