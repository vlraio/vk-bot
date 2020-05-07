from server import Server
from config import vk_api_token as token

server = Server(token, "Server 1")
server.start()
