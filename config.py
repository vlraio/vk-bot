#  VK API токен для доступа
vk_api_token = "Your vk api..."

#  Сайт, с которого взяты данные
web_schedule_link = "https://www.mirea.ru/schedule/"

#  Ссылка на папку с хранилищем таблицы исходника
excel_table_path = "schedule/tables/"

#  Ссылка на папку с хранилищем json файлов с расписанием
json_data_path = "schedule/json-files-data/"

#  Дата начала обучения в семестре
start_study_date = "2020-02-10"

#  Ссылки на json файлы с клавиатурами
JSON_CLEAR = "keyboards/clear.json"
JSON_SCHEDULE = "keyboards/schedule.json"

#  Папки, где хранятся excel таблицы
schedule_list = ["1 курс", "2 курс", "3 курс"]

#  Словарь с переводом дней недели с английского на русский для получения данных из json
week_day_dict = {"Понедельник": "Monday", "Вторник": "Tuesday", "Среда": "Wednesday",
                 "Четверг": "Thursday", "Пятница": "Friday", "Суббота": "Saturday"}

GROUP_REGEX = r"[и,И]{1}[а,А,в,В,к,К,н,Н]{1}[б,Б]{1}[о,О]{1}([-]|[ ])([0-9]){2}([-]|[ ])1([7-9]){1}"
