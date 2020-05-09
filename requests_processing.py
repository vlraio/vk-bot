from datetime import datetime, timedelta
import locale
import re

from requests_list import RequestsList
from schedule_func import Schedule
from config import GROUP_REGEX, week_day_dict


#  TODO: доделать оставшиеся задания из пунктов
#  Обработка всех команд
class Command:

    def __init__(self):
        self.new = True
        self.group = None

    def get_group(self):
        return self.group

    def input(self, message, vk_api, user_id):
        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
        today = datetime.today()

        #  Приветствие пользователя
        if message.lower() in RequestsList.greetings:
            response = Schedule.greeting(vk_api, user_id, self.new)
            self.new = False
            return response

        #  Проверка на нового пользователя для ввода номера группы
        if self.group is None:
            if re.match(GROUP_REGEX, message) is None:
                return "Вы неправильно ввели номер группы!\nПопробуйте ещё раз."
            self.group = message.upper().replace(" ", "-")
            return "Ваша группа {}.\nНапишите 'Бот' для старта.".format(self.group)

        elif message == "Бот":
            return "Бот готов!"

        #  Номер группы
        elif message == "Какая группа?":
            return "Вы обучаетесь в группе {}.".format(self.group)

        #  Номер недели
        elif message == "Какая неделя?":
            return "Идет {} неделя.".format(Schedule.count_week_num())

        #  Расписание на сегодня
        elif message == "На сегодня":
            #  Определение четности/нечетности недели (0 - н/ч; 1 - ч)
            week_type = int(not Schedule.count_week_num() % 2)
            return Schedule.get_response_schedule(self.group, today, week_type, True)

        #  Расписание на завтра
        elif message == "На завтра":
            week_type = int(not Schedule.count_week_num() % 2)
            tomorrow = today + timedelta(days=1)
            return Schedule.get_response_schedule(self.group, tomorrow, week_type, True)

        #  Расписание на текущую неделю
        elif message == "На эту неделю":
            #  Первый день текущей недели
            start = today - timedelta(days=today.weekday())
            week_type = int(not Schedule.count_week_num() % 2)
            return Schedule.get_response_schedule(self.group, start, week_type)

        #  Расписание на следующую неделю
        elif message == "На следующую неделю":
            start = today + timedelta(days=7) - timedelta(days=today.weekday())
            week_type = int(Schedule.count_week_num() % 2)
            return Schedule.get_response_schedule(self.group, start, week_type)

        elif re.match(r"Бот [А-Я,а-я]+", message):
            mes = message.replace("Бот ", "").replace(" ", "-").split()

            #  Проверка на ввод "Бот <день_недели>"
            if mes[0].title() in week_day_dict.keys() != "-" and len(mes[0]) <= 11 and re.match(r"[а-я]{5,}", mes[0]):
                return Schedule.get_response_for_day_schedule(self.group, mes[0])

            #  Проверка на ввод "Бот <номер_группы>"
            elif re.match(GROUP_REGEX, mes[0]):
                self.group = mes[0].upper()
                return "Доступно расписание для группы {}.".format(self.group)

            #  Проверка на ввод "Бот <день_недели номер_группы>"
            else:
                arr = mes[0].replace("-", " ", 1).split()
                if arr[0].title() in week_day_dict.keys() and re.match(r"[а-я]{5,}", arr[0]) and re.match(GROUP_REGEX, arr[1]):
                    return Schedule.get_response_for_day_schedule(arr[1].upper(), arr[0])

        return "Неверно введена команда."
