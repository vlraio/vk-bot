import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from requests_processing import Command
from config import JSON_CLEAR, JSON_SCHEDULE


class Launcher:

    def __init__(self, token):
        self.__vk = vk_api.VkApi(token=token)  # Для работы с long poll
        self.__longpoll = VkLongPoll(self.__vk)  # Использование long poll api
        self.__vk_api = self.__vk.get_api()  # Использование методов из vk_api
        self.__users = {}  # Словарь из пользователей (ключ) и последней команды (значение) (в дальнейшем - База Данных)
        self.__json_kb = JSON_CLEAR

    def send_message(self, user_id, message):
        self.__vk_api.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            keyboard=open(self.__json_kb, "r", encoding="UTF-8").read(),
            message=message)

    def start(self):
        print("App started...")
        for event in self.__longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
                uid = event.user_id

                if uid not in self.__users:
                    self.__users[uid] = Command()

                if event.text == "Бот" and Command.get_group(self.__users[uid]) is not None:
                    self.__json_kb = JSON_SCHEDULE

                self.send_message(uid, self.__users[uid].input(event.message, self.__vk_api, uid))

