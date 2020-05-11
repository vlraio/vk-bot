from config import fake_db_path
from datetime import datetime, timedelta


class UpdatesFakeDataBase:

    @staticmethod
    def check():
        path = "{}/schedule_fake_db.txt".format(fake_db_path)

        with open(path, "r", encoding="UTF-8") as f:
            last_update = f.read()
            f.close()

        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        if last_update < yesterday:
            with open(path, "w", encoding="UTF-8") as f:
                f.write(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
                f.close()
                return True
        return False
