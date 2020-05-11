import requests as rq
from bs4 import BeautifulSoup
import re

from config import link_covid


#  Получение статистики с сайта
class ReceiveCovid:

    def __init__(self):
        self.days = []

        self.active = []
        self.cured = []
        self.died = []
        self.total = []

        self.active_plus = []
        self.cured_plus = []
        self.died_plus = []
        self.total_plus = []

        self.upd_date = ""

    def start(self):
        page = rq.get(link_covid)
        soup = BeautifulSoup(page.text, "html.parser")
        response = soup.findAll("table")[0].find("tbody").findAll("tr")

        self.days = re.findall(r"<th>(.*?)</th>", str(response))

        self.active = ReceiveCovid.get(r" {2,}\d+", response, 0)
        self.cured = ReceiveCovid.get(r" {2,}\d+", response, 1)
        self.died = ReceiveCovid.get(r" {2,}\d+", response, 2)
        self.total = ReceiveCovid.get(r" {2,}\d+", response, 3)

        self.active_plus = ReceiveCovid.get(r">\W\d+<", response, 0)
        self.cured_plus = ReceiveCovid.get(r">\W\d+<", response, 1)
        self.died_plus = ReceiveCovid.get(r">\W\d+<", response, 2)
        self.total_plus = ReceiveCovid.get(r">\W\d+<", response, 3)

        response = soup.find("h6", {"class": "text-muted"})
        self.upd_date = re.findall(r"<strong>(.*?)</strong>", str(response), re.DOTALL)[0]

    @staticmethod
    def get(regex, response, i):
        x = []
        for r in response:
            num = r.findAll("td")
            x.append(re.findall(regex, str(num))[i].replace(" ", "").replace(">", "").replace("<", ""))
        x.reverse()
        return x

