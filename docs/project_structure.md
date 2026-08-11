# Структура проекта RUNNING-INSIGHTS

---
## `run.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\__init__.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\prepare\__init__.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\prepare\create_races_catalog.py`
&nbsp;&nbsp;&nbsp;&nbsp;**build_raw_race_catalog()** | Создает черновой каталог забегов из сырых данных RussiaRunning. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**build_race_catalog()** | Формирует расширенный каталог забегов на основе <br>

---
## `src\scraper\__init__.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\scraper\api.py`
&nbsp;&nbsp;&nbsp;&nbsp;**get_event_page()** | Получает одну страницу списка мероприятий RussiaRunning. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**get_event()** | Получает подробную информацию о мероприятии RussiaRunning. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**get_participants_page()** | Получает одну страницу участников выбранной дистанции. <br>

---
## `src\scraper\event_filter.py`
&nbsp;&nbsp;&nbsp;&nbsp;**filter_events()** | Исключает из списка мероприятия, которые не должны участвовать <br>

---
## `src\scraper\event_parser.py`
&nbsp;&nbsp;&nbsp;&nbsp;**parse_event_page()** | Извлекает список мероприятий из ответа API. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**extract_races()** | Извлекает информацию о дистанциях мероприятия. <br>

---
## `src\scraper\main.py`
&nbsp;&nbsp;&nbsp;&nbsp;**main()** | Без описания <br>
&nbsp;&nbsp;&nbsp;&nbsp;**collect_participants()** | Собирает всех участников одной дистанции. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**collect_events()** | Собирает список мероприятий с сайта RussiaRunning. <br>

---
## `src\scraper\participant_parser.py`
&nbsp;&nbsp;&nbsp;&nbsp;**parse_participants_page()** | Извлекает участников из одной страницы ответа API. <br>

---
## `src\storage\__init__.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\storage\json_writer.py`
&nbsp;&nbsp;&nbsp;&nbsp;**save_json()** | Сохраняет список словарей в JSON-файл. <br>

---
## `src\tools\project_structure_generator.py`
&nbsp;&nbsp;&nbsp;&nbsp;**get_functions()** | Извлекает список функций верхнего уровня из Python-файла. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**generate_project_structure()** | Генерирует Markdown-документацию со структурой проекта. <br>

---
## `src\transform\__init__.py`
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## `src\transform\build_dataset.py`
&nbsp;&nbsp;&nbsp;&nbsp;**merge_participant_references()** | Добавляет к данным участников расшифровки статусов и пола. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**merge_events()** | Добавляет к данным участников информацию о мероприятиях. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**merge_race_catalog()** | Добавляет к данным о забегах информацию из каталога. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**merge_races()** | Добавляет к данным участников информацию о дистанциях, <br>
&nbsp;&nbsp;&nbsp;&nbsp;**select_and_rename_columns()** | Выбирает колонки, необходимые для итогового аналитического <br>
&nbsp;&nbsp;&nbsp;&nbsp;**main()** | Формирует итоговый датасет участников. <br>

---
## `src\transform\build_participants.py`
&nbsp;&nbsp;&nbsp;&nbsp;**build_participants()** | Объединяет данные об участниках из отдельных JSON-файлов <br>
