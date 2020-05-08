from bs4 import BeautifulSoup
import requests as rq
import re

from config import web_schedule_link, excel_table_path


#  Получение данных (расписание) с сайта
class ReceiveData:

    @staticmethod
    def start():
        page = rq.get(web_schedule_link)
        soup = BeautifulSoup(page.text, "html.parser")
        response = soup.find("div", {"class": "rasspisanie"}).find(
            string="Институт информационных технологий").find_parent(
            "div").find_parent("div").find_all("a", {"class": "uk-link-toggle"})

        # TODO: исправить проверки на получение данных (с помощью РЕГУЛЯРНЫХ выражений)
        for r in response:
            if re.match(r"(http|https)://(.*?)(ИИТ_)(.*?)(.xlsx)", r["href"]) is not None:
                title = r.find("div", {"class": "uk-link-heading uk-margin-small-top"})
                title = re.findall(r"\d [а-я]+", str(title))[0]

                f = open("{0}{1}.xlsx".format(excel_table_path, title), "wb")
                f.write(rq.get(r["href"]).content)
                f.close()
