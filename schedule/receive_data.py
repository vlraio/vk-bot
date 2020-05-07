from bs4 import BeautifulSoup
import requests as rq

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
            if "ИИТ" in str(r) and ".xlsx" in str(r) and "1к" in str(r):
                to_print = r["href"]
                f = open(excel_table_path, "wb")
                f.write(rq.get(r["href"]).content)
                f.close()
