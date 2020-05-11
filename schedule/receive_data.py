from bs4 import BeautifulSoup
import requests as rq
import re

from config import web_schedule_link, excel_table_path
from updates.updates import UpdatesFakeDataBase
from schedule.parse_data import ParseSchedule


#  Получение расписания с сайта
class ReceiveSchedule:

    @staticmethod
    def start(s_list):

        if not UpdatesFakeDataBase.check():
            return None

        page = rq.get(web_schedule_link)
        soup = BeautifulSoup(page.text, "html.parser")
        response = soup.find("div", {"class": "rasspisanie"}).find(
            string="Институт информационных технологий").find_parent(
            "div").find_parent("div").find_all("a", {"class": "uk-link-toggle"})

        for r in response:
            if re.match(r"(http|https)://(.*?)(ИИТ_)(.*?)(.xlsx)", r["href"]) is not None:
                title = r.find("div", {"class": "uk-link-heading uk-margin-small-top"})
                title = re.findall(r"\d [а-я]+", str(title))[0]

                f = open("{0}{1}.xlsx".format(excel_table_path, title), "wb")
                f.write(rq.get(r["href"]).content)
                f.close()
        print("Schedule was updated")
        ParseSchedule.start(s_list)
