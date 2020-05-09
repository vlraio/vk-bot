import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from requests_processing import Command
from config import JSON_CLEAR, JSON_SCHEDULE, JSON_WEATHER


class Launcher:

    def __init__(self, token):
        self.vk = vk_api.VkApi(token=token)  # Для работы с long poll
        self.longpoll = VkLongPoll(self.vk)  # Использование long poll api
        self.vk_api = self.vk.get_api()  # Использование методов из vk_api
        self.users = {}  # Словарь из пользователей (ключ) и последней команды (значение)
        self.json_kb = JSON_CLEAR

    def send_message(self, user_id, message):
        self.vk_api.messages.send(
            user_id=user_id,
            random_id=get_random_id(),
            keyboard=open(self.json_kb, "r", encoding="UTF-8").read(),
            message=message)

    def start(self):
        print("App started...")
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
                uid = event.user_id

                if uid not in self.users:
                    self.users[uid] = Command()

                if event.text == "Бот" and Command.get_group(self.users[uid]) is not None:
                    self.json_kb = JSON_SCHEDULE

                if event.text == "Погода":
                    self.json_kb = JSON_WEATHER

                self.send_message(uid, self.users[uid].input(event.message, self.vk_api, uid))

