import json

from config import json_schedule_path


#  Модель для общения с данными расписания
class Group:
    def __init__(self, name):
        self.name = name
        self.schedule = None

    def set_schedule(self, sch):
        f = open("{0}{1}.json".format(json_schedule_path, self.name), "w")
        save = json.dumps(sch, ensure_ascii=False, indent=4)
        f.write(save)
        f.close()
        self.schedule = save

    @staticmethod
    def get_schedule_by_name(name):
        try:
            with open("{0}{1}.json".format(json_schedule_path, name), "r", encoding="UTF-8") as f:
                text = json.load(f)
                return text
        except FileNotFoundError:
            return None
