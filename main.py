from config import schedule_list, vk_api_token as token
from schedule.receive_data import ReceiveData
from schedule.parse_data import ParseData
from launcher import Launcher

# ReceiveData.start()
# ParseData.start(schedule_list)

launcher = Launcher(token)
launcher.start()
