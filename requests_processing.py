from datetime import datetime, timedelta
import locale
import re

from requests_list import RequestsList
from schedule_func import Schedule


#  TODO: доделать оставшиеся задания из пунктов
#  Обработка всех команд
class Command:

    def __init__(self):
        self.__new = True
        self.__group = None

    def get_group(self):
        return self.__group

    def input(self, message, vk_api, user_id):
        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
        today = datetime.today()

        #  Приветствие пользователя
        if message.lower() in RequestsList.greetings:
            response = Schedule.greeting(vk_api, user_id, self.__new)
            self.__new = False
            return response

        #  Проверка на нового пользователя для ввода номера группы
        if self.__group is None:
            if re.match(r"([а-я]|[А-Я]){4}([-]|[ ])([0-9]){2}([-]|[ ])([0-9]){2}", message) is None:
                return "Вы неправильно ввели номер группы!\nПопробуйте ещё раз."
            self.__group = message.upper().replace(" ", "-")
            return "Ваша группа {}.\nНапишите 'Бот' для старта.".format(self.__group)

        elif message == "Бот":
            return "Бот готов!"

        #  Номер группы
        elif message == "Какая группа?":
            return "Вы обучаетесь в группе {}.".format(self.__group)

        #  Номер недели
        elif message == "Какая неделя?":
            return "Идет {} неделя.".format(Schedule.count_week_num())

        #  Расписание на сегодня
        elif message == "На сегодня":
            #  Определение четности/нечетности недели (0 - н/ч; 1 - ч)
            week_type = int(not Schedule.count_week_num() % 2)
            return Schedule.get_response(self.__group, today, week_type, True)

        #  Расписание на завтра
        elif message == "На завтра":
            week_type = int(not Schedule.count_week_num() % 2)
            tomorrow = today + timedelta(days=1)
            return Schedule.get_response(self.__group, tomorrow, week_type, True)

        #  Расписание на текущую неделю
        elif message == "На эту неделю":
            #  Первый день текущей недели
            start = today - timedelta(days=today.weekday())
            week_type = int(not Schedule.count_week_num() % 2)
            return Schedule.get_response(self.__group, start, week_type)

        #  Расписание на следующую неделю
        elif message == "На следующую неделю":
            start = today + timedelta(days=7) - timedelta(days=today.weekday())
            week_type = int(Schedule.count_week_num() % 2)
            return Schedule.get_response(self.__group, start, week_type)
