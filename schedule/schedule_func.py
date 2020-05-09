from datetime import datetime, timedelta, date
import locale

from config import start_study_date, week_day_dict
from schedule.group import Group


#  Обработка запросов по расписанию
class Schedule:

    #  Функция приветствия пользователя
    @staticmethod
    def greeting(vk_api, user_id, new):
        day_time = datetime.now().hour
        response = "Добрый день"
        if 5 < day_time < 12:
            response = "Доброе утро"
        if 17 < day_time < 24:
            response = "Добрый вечер"
        if day_time < 6:
            response = "Доброй ночи"
        s = vk_api.users.get(user_id=user_id)[0]["first_name"]
        response = "{0}, {1}!".format(response, s)

        if new:
            return "{}\nВведите номер своей группы.".format(response)
        return response

    #  Цикл по составлению расписания
    @staticmethod
    def get_schedule(value, week_type):
        response = ""
        for i in range(len(value)):
            if value[i][week_type]["subject"] == "-":
                response += "{}) -\n".format(i + 1)
            else:
                #  value[<номер_пары>][<ч_н/ч_неделя>]["<ключ>"]
                response += "{5}) {0}, {1}, {2}, {3}, {4}\n" \
                    .format(value[i][week_type]["subject"],
                            value[i][week_type]["sub_type"],
                            value[i][week_type]["professor"],
                            value[i][week_type]["room"],
                            value[i][week_type]["link"], i + 1)
        return response

    #  Составление ответа по расписанию (на сегодня/завтра/неделю)
    @staticmethod
    def get_response_schedule(group, day, week_type, one_day: bool = False):
        response = ""
        if one_day:
            for key, value in Group.get_schedule_by_name(group).items():
                locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
                if key == day.strftime("%A"):
                    locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
                    response += "\nРасписание на {} {} {}\n".format(
                        day.strftime("%A").replace("а", "у"), day.day, day.strftime("%B").title())
                    response += Schedule.get_schedule(value, week_type)
                    return response
            return "Выходной день. Отдыхайте! :)"

        for key, value in Group.get_schedule_by_name(group).items():
            response += "\nРасписание на {} {} {}\n".format(
                day.strftime("%A").replace("а", "у"), day.day, day.strftime("%B").title())
            day += timedelta(days=1)
            response += Schedule.get_schedule(value, week_type)
        return response

    #  Подсчет номера недели
    @staticmethod
    def count_week_num():
        d = start_study_date.split("-")
        start = date(int(d[0]), int(d[1]), int(d[2]))
        days = abs(date.today() - start).days
        return days // 7 + 1

    #  Составление ответа по расписанию (на заданный день)
    @staticmethod
    def get_response_for_day_schedule(group, week_day):
        response = ""
        for key, value in Group.get_schedule_by_name(group).items():
            if key == week_day_dict.get(week_day.title()):
                response += "\nРасписание на {} (н/ч)\n".format(week_day.replace("а", "у"))
                response += Schedule.get_schedule(value, 0)
                response += "\nРасписание на {} (ч)\n".format(week_day.replace("а", "у"))
                response += Schedule.get_schedule(value, 1)
                return response
