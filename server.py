import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from requests_processing import Command


class Server:

    def __init__(self, token, name: str = "Server"):
        self.__vk = vk_api.VkApi(token=token)  # Для работы с long poll
        self.__longpoll = VkLongPoll(self.__vk)  # Использование long poll api
        self.__vk_api = self.__vk.get_api()  # Использование методов из vk_api
        self.__server_name = name  # Название сервера
        self.__users = {}  # Словарь из пользователей (ключ) и последней команды (значение) (в дальнейшем - База Данных)

    def send_message(self, user_id, message):
        print(message)
        self.__vk_api.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            message=message)

    def start(self):
        for event in self.__longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
                uid = event.user_id

                if uid not in self.__users:
                    self.__users[uid] = Command()

                self.send_message(uid, self.__users[uid].input(event.message, self.__vk_api, uid))

