
#  VK api токен для доступа
vk_api_token = "7b8973a3a6009cabb4e1298a69f92c46a34f3d9964283fbf34c74b80f597121dd17fa023f0999dbbfcacf"

#  OpenWeather api вызов
weather_api_call = "https://api.openweathermap.org/data/2.5/{" \
                   "}?q=moscow&appid=d4caf1ea454415eb6df2072162f25fec&units=metric&lang=ru"

#  Ссылка на картинки по погоде
weather_link_png = "https://openweathermap.org/img/wn/{}.png"
#  "https://openweathermap.org/img/wn/{}@2x.png"
#  Сайт, с которого взяты данные
web_schedule_link = "https://www.mirea.ru/schedule/"

#  Ссылка на папку с хранилищем таблицы исходника
excel_table_path = "schedule/tables/"

#  Ссылки на папки с хранилищем json файлов
json_schedule_path = "schedule/json-files-data/"
json_weather_path = "weather/json-files-data/"
icons_path = "weather/icons/"

#  Дата начала обучения в семестре
start_study_date = "2020-02-10"

#  Папки, где хранятся excel таблицы
schedule_list = ["1 курс", "2 курс", "3 курс"]

#  Словарь с переводом дней недели с английского на русский для получения данных из json
week_day_dict = {"Понедельник": "Monday", "Вторник": "Tuesday", "Среда": "Wednesday",
                 "Четверг": "Thursday", "Пятница": "Friday", "Суббота": "Saturday"}

#  Словарь с данными по шкале Бофорта
wind_beaufort_dict = {"штиль": [0.0, 0.2], "тихий": [0.3, 1.5], "легкий": [1.6, 3.3],
                      "слабый": [3.4, 5.4], "умеренный": [5.5, 7.9], "свежий": [8.0, 10.7],
                      "сильный": [10.8, 13.8], "крепкий": [13.9, 17.1], "очень крепкий": [17.2, 20.7],
                      "шторм": [20.8, 24.4], "сильный шторм": [24.5, 28.4], "жесткий шторм": [28.5, 32.6],
                      "ураган": [33.0, 115.0]}

#  Словарь с данными по напрвлению ветра (румб)
wind_rumb_dict = {"северный": [0.0, 44.99], "северо-восточный": [45.0, 89.99], "восточный": [90.0, 134.99],
                  "юго-восточный": [135.0, 179.99], "южный": [180.0, 224.99], "юго-западный": [225.0, 269.99],
                  "западный": [270.0, 314.99], "северо-западный": [315.0, 360.0]}

#  Регулярное выражение для выбора номера группы
GROUP_REGEX = r"[и,И]{1}[а,А,в,В,к,К,н,Н]{1}[б,Б]{1}[о,О]{1}([-]|[ ])([0-9]){2}([-]|[ ])1([7-9]){1}"

#  Ссылки на json файлы с клавиатурами
JSON_CLEAR = "keyboards/clear.json"
JSON_SCHEDULE = "keyboards/schedule.json"
JSON_WEATHER = "keyboards/weather.json"
