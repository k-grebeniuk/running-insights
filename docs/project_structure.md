# Структура проекта RUNNING-INSIGHTS

---
## scraper\__init__.py
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**

---
## scraper\browser.py
&nbsp;&nbsp;&nbsp;&nbsp;**create_browser()** | Создает экземпляр браузера Chromium. <br>

---
## scraper\event_parser.py
&nbsp;&nbsp;&nbsp;&nbsp;**select_event_filter()** | Выбирает фильтр "Забег" в списке мероприятий. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**parse_events()** | Извлекает список мероприятий со страницы результатов. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**normalize_url()** | Преобразует относительные ссылки в абсолютные. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**select_distance()** | ОПИСАНИЕ!!! <br>
&nbsp;&nbsp;&nbsp;&nbsp;**normalize_distance()** | Приводит название дистанции к единому виду. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**get_distances()** | Извлекает список дистанций мероприятия. <br>

---
## scraper\main.py
&nbsp;&nbsp;&nbsp;&nbsp;**main()** | Без описания <br>
&nbsp;&nbsp;&nbsp;&nbsp;**collect_participants()** | Собирает участников мероприятия по всем выбранным дистанциям. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**collect_events()** | Собирает список мероприятий. <br>

---
## scraper\paginator.py
&nbsp;&nbsp;&nbsp;&nbsp;**get_last_page()** | Определяет номер последней страницы пагинации. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**go_to_page()** | Переходит на указанную страницу пагинации. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**get_current_page()** | Получает номер текущей активной страницы пагинации. <br>

---
## scraper\parser.py
&nbsp;&nbsp;&nbsp;&nbsp;**get_headers()** | Извлекает названия колонок таблицы участников. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**parse_rows()** | Извлекает данные участников из строк таблицы. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**parse_participants()** | Полностью извлекает участников из таблицы результатов <br>

---
## scraper\scraper_summary.py
&nbsp;&nbsp;&nbsp;&nbsp;**get_functions()** | Возвращает список функций файла: <br>
&nbsp;&nbsp;&nbsp;&nbsp;**generate_project_structure()** | Генерирует Markdown-документацию со структурой проекта. <br>

---
## scraper\storage.py
&nbsp;&nbsp;&nbsp;&nbsp;**save_participants()** | Сохраняет результаты участников мероприятия в CSV-файл. <br>
&nbsp;&nbsp;&nbsp;&nbsp;**save_events()** | Сохраняет информацию о мероприятиях в CSV-файл. <br>

---
## transform\__init__.py
&nbsp;&nbsp;&nbsp;&nbsp;**Нет функций**
