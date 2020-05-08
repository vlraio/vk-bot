import xlrd
import re

from schedule.group import Group
from config import excel_table_path


#  Сериализация данных (расписание) в json файлы
class ParseData:

    @staticmethod
    def operate(f):
        book = xlrd.open_workbook("{0}{1}.xlsx".format(excel_table_path, f))
        sheet = book.sheet_by_index(0)

        num_columns = sheet.ncols

        groups_list = []
        week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        for col_id in range(num_columns):
            group_cell = str(sheet.cell(1, col_id).value)
            if "БО-" in group_cell:
                g = Group(group_cell)
                groups_list.append(g)
                week = {"Monday": None, "Tuesday": None, "Wednesday": None, "Thursday": None, "Friday": None,
                        "Saturday": None}
                for les in range(6):
                    day = [[], [], [], [], [], []]
                    for i in range(len(week_days)):
                        for j in range(2):
                            subject = sheet.cell(3 + j + i * 2 + les * 12, col_id).value
                            sub_type = sheet.cell(3 + j + i * 2 + les * 12, col_id + 1).value
                            professor = sheet.cell(3 + j + i * 2 + les * 12, col_id + 2).value
                            room = sheet.cell(3 + j + i * 2 + les * 12, col_id + 3).value
                            link = sheet.cell(3 + j + i * 2 + les * 12, col_id + 4).value

                            subject = re.sub(r"(?:(?<=кр. )|(?<=кр ))(.*?)(?= н.)", "", subject)
                            subject = re.sub(r"((кр. )|(кр )).*?(н. )", "", subject)
                            subject = re.sub(r"^(?!кр.*$).*?(?= н.)", "", subject)
                            subject = re.sub(r"^(?!кр.*$).*?( н. )", "", subject)
                            subject = subject.replace("\n", " ")

                            if subject == "":
                                subject = "-"
                            if sub_type == "":
                                sub_type = "-"
                            if professor == "":
                                professor = "-"
                            if room == "":
                                room = "-"
                            if link == "":
                                link = "-"
                            lesson = {"subject": subject, "sub_type": sub_type, "professor": professor, "room": room,
                                      "link": link}
                            day[i].append(lesson)
                    week[week_days[les]] = day
                g.set_schedule(week)

    @staticmethod
    def start(folders_list):
        for folder in folders_list:
            ParseData.operate(folder)
