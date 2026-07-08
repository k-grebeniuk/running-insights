from browser import create_browser
from paginator import (
    get_last_page,
    go_to_page,
    get_current_page,
)
from parser import parse_participants
from storage import (
    save_participants,
    save_events
)
from event_parser import (
    select_event_filter,
    parse_events
)



URL = "https://heroleague.ru/results/zabeg2026_554234"      #Зеленоградск
#URL = "https://heroleague.ru/results/zabeg2026_498817"      #Санкт-Петербург


def main():
    playwright, browser, page = create_browser()


    try:
        page.goto(URL)
        page.wait_for_selector("nav[aria-label='Countries Pagination']")

        page.wait_for_timeout(2000)
        last_page = get_last_page(page)

        print("Последняя страница:", last_page)


        for page_num in range(1, last_page + 1):

            print(f"Парсим страницу {page_num}/{last_page}")

            # переходим на нужную страницу
            go_to_page(page,page_num)

            # проверяем, что реально перешли
            current = get_current_page(page)
            print(f"Текущая страница: {current}")

            # извлекаем участников
            participants = parse_participants(page)
            print(f"Получено участников: {len(participants)}")

            # сохраняем в CSV
            save_participants(participants,'event_id')


    finally:
        browser.close()
        playwright.stop()


RESULTS_URL = "https://heroleague.ru/results"


def collect_events() -> None:
    """
    Собирает список всех мероприятий и сохраняет его в CSV.

    Последовательность работы:
        1. Открывает браузер.
        2. Переходит на страницу результатов.
        3. Выбирает фильтр «Забег».
        4. Извлекает данные о мероприятиях.
        5. Сохраняет их в файл.
        6. Закрывает браузер.

    Returns:
        None:
            Функция сохраняет данные и ничего не возвращает.
    """

    playwright, browser, page = create_browser()

    try:
        page.goto(RESULTS_URL)

        page.wait_for_timeout(2000)

        select_event_filter(page)

        events = parse_events(page)

        #добавляем id для каждого мероприятия
        for event_id, event in enumerate(events, start=1):
            event["event_id"] = event_id

        save_events(events)


    finally:
        browser.close()
        playwright.stop()


if __name__ == "__main__":
    collect_events()