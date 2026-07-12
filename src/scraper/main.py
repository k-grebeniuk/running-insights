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
    parse_events,
    select_distance
)
from event_parser import get_distances
from playwright.sync_api import Page


def main():

    RESULTS_URL = "https://heroleague.ru/results"

    DISTANCES = [
        "1 km",
        "5 km",
        "10 km",
        "21.1 km"
    ]

    playwright, browser, page = create_browser()

    try:
        events = collect_events(page, RESULTS_URL)

        save_events(events)

        for event in events:
            if event['url'].startswith('https://heroleague.ru/results'):
                collect_participants(page, event)

    finally:
        browser.close()
        playwright.stop()



def collect_participants(
    page: Page,
    event: dict
) -> None:
    """
    Собирает участников мероприятия по всем выбранным дистанциям.

    Функция открывает страницу результатов мероприятия,
    последовательно переключает дистанции, проходит по всем
    страницам результатов и сохраняет найденных участников.

    Args:
        page (Page):
            Открытая страница браузера Playwright.

        event (dict):
            Словарь с информацией о мероприятии.
            Должен содержать:
                - event_id
                - name
                - city
                - url

        distances (list[str]):
            Список дистанций для сбора участников.
            Например:
                [
                    "1 km",
                    "5 km",
                    "10 km",
                    "21.1 km"
                ]

    Returns:
        None
    """

    page.goto(event["url"])

    print(f"\nСбор участников: {event['name']} ({event['city']})")

    page.wait_for_selector("nav[aria-label='Countries Pagination']")

    event_participants = 0

    distances = get_distances(page)

    for distance, site_distance in distances.items():

        print(f"\nДистанция: {distance}")

        if not select_distance(page, site_distance):
            print(f'Не удалось выбрать "{distance}"')
            continue

        page.wait_for_timeout(2000)

        last_page = get_last_page(page)
        print("Страниц:", last_page)

        distance_participants = 0
        for page_num in range(1, last_page + 1):

            print(f"  Страница {page_num}/{last_page}")

            # переходим на нужную страницу
            go_to_page(page,page_num)

            # извлекаем участников
            participants = parse_participants(page, event['event_id'], distance)

            # считаем количество участников
            distance_participants += len(participants)

            # сохраняем в CSV
            event_id = f"{event['name']} ({event['city']})"
            save_participants(participants, event_id)

        print(f'Участников на дистанции {distance}: {distance_participants}')
        event_participants += distance_participants

    print(f"Количество участников в {event['name']} ({event['city']}): {event_participants}")



def collect_events(
    page: Page,
    results_url: str
) -> list[dict]:
    """
    Собирает список мероприятий.

    Последовательность работы:
        1. Переходит на страницу результатов.
        2. Выбирает фильтр «Забег».
        3. Извлекает данные о мероприятиях.
        4. Добавляет уникальный event_id каждому мероприятию.
        5. Возвращает список мероприятий.

    Args:
        page (Page):
            Открытая страница Playwright.

        results_url (str):
            Ссылка на страницу результатов.

    Returns:
        list[dict]:
            Список мероприятий.
            Каждый элемент содержит данные мероприятия
            и уникальный event_id.
    """

    page.goto(results_url)

    page.wait_for_timeout(2000)

    select_event_filter(page)

    events = parse_events(page)

    # Добавляем id для каждого мероприятия
    for event_id, event in enumerate(events, start=1):
        event["event_id"] = event_id

    return events


if __name__ == "__main__":
    main()