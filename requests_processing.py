from requests_list import RequestsList
import datetime as dt

from schedule.group import get_schedule_by_name


def greeting(vk_api, user_id, new):
    day_time = dt.datetime.now().hour
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


class Command:

    def __init__(self):
        self.__new = True
        self.__group = ""

    def input(self, message, vk_api, user_id):
        #  Приветствие бота
        if message.lower() in RequestsList.greetings:
            response = greeting(vk_api, user_id, self.__new)
            self.__new = False
            return response

        #  Проверка на нового пользователя для ввода номера группы
        if self.__group == "":
            self.__group = message.upper().replace(" ", "-")
            return "Ваша группа {}.".format(self.__group)

        if message == "Дай":
            print(self.__group)
            return get_schedule_by_name(self.__group)


