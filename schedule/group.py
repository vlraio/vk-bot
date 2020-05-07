import json
from config import json_data_path as json_path


def get_schedule_by_name(name):
    with open("schedule/{0}{1}.json".format(json_path, name), "r", encoding="UTF-8") as f:
        text = json.load(f)
        return text


class Group:
    def __init__(self, name):
        self.__name = name
        self.__schedule = None

    def set_schedule(self, sch):
        f = open("{0}{1}.json".format(json_path, self.__name), "w")
        save = json.dumps(sch, ensure_ascii=False, indent=4)
        f.write(save)
        f.close()
        self.__schedule = save

    def get_name(self):
        return self.__name

    def get_schedule(self):
        return self.__schedule
