import re

from weather.receive_data import ReceiveWeather
from requests_list import RequestsList
from schedule.schedule_func import Schedule
from config import GROUP_REGEX
from mode_bot import Mode
from modes import ModeWork


#  TODO: доделать оставшиеся задания из пунктов
#  Обработка всех команд
class Command:

    def __init__(self):
        self.mode = None
        self.new = True
        self.group = None

    def get_group(self):
        return self.group

    def input(self, message, vk_api, user_id):
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
            return "Ваша группа {}.\nНапишите 'Бот' для работы с расписанием." \
                   "\nНапишите 'Погода' для работы с погодой.".format(self.group)

        #  Выбор режима пользователем
        elif message.lower() == "бот":
            self.mode = Mode.schedule
            return "Режим расписания включен."

        elif message.lower() == "погода":
            self.mode = Mode.weather
            ReceiveWeather.start("weather")
            ReceiveWeather.start("forecast")
            #  Загрузка иконок из интернета
            #  ReceiveWeather.load_icons()
            return "Режим погоды включен."

        elif message.lower() == "ковид":
            self.mode = Mode.covid
            return ModeWork.covid()

        if self.mode == Mode.schedule:
            response, self.group = ModeWork.schedule(message, self.group)
            return response

        if self.mode == Mode.weather:
            return ModeWork.weather(message)


        return "Такого режима нет."
