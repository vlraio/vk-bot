import xlrd
from schedule.group import Group
from config import excel_table_path

book = xlrd.open_workbook(excel_table_path)
sheet = book.sheet_by_index(0)

num_columns = sheet.ncols
num_rows = sheet.nrows

groups_list = []
groups = {}
week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

for col_id in range(num_columns):
    group_cell = str(sheet.cell(1, col_id).value)
    if "-19" in group_cell and "БО" in group_cell:
        g = Group(group_cell)
        groups_list.append(g)
        week = {"Monday": None, "Tuesday": None, "Wednesday": None, "Thursday": None, "Friday": None, "Saturday": None}
        for les in range(6):
            day = [[], [], [], [], [], []]
            for i in range(len(week_days)):
                for j in range(2):
                    subject = sheet.cell(3 + j + i * 2 + les * 12, col_id).value
                    sub_type = sheet.cell(3 + j + i * 2 + les * 12, col_id + 1).value
                    professor = sheet.cell(3 + j + i * 2 + les * 12, col_id + 2).value
                    room = sheet.cell(3 + j + i * 2 + les * 12, col_id + 3).value
                    link = sheet.cell(3 + j + i * 2 + les * 12, col_id + 4).value
                    lesson = {"subject": subject, "sub_type": sub_type, "professor": professor, "room": room,
                              "link": link}
                    day[i].append(lesson)
            week[week_days[les]] = day
        g.set_schedule(week)
