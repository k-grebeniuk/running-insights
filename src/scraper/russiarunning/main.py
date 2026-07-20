from src.scraper.russiarunning.api import (get_event_page,
                                           get_event)
from src.scraper.russiarunning.event_parser import (parse_event_page,
                                                    extract_races)
from src.scraper.russiarunning.event_filter import filter_events
from src.storage.json_writer import save_json

from pathlib import Path


def main():
    all_events = collect_events()
    filtered_events  = filter_events(all_events)

    save_json(
        filtered_events ,
        Path("data/raw/russiarunning/events.json"),
    )

    races = []

    for event in filtered_events:
        event_data = get_event(event["code"])
        event_races = extract_races(event_data)

        for race in event_races:
            race["event_id"] = event["id"]
            race["event_code"] = event["code"]
            race["event_title"] = event["title"]
            
        print(event["title"])
        for race in event_races:
            print(race)        
        print()

        races.extend(event_races)

    save_json(
        races,
        Path("data/raw/russiarunning/races.json"),
    )

def collect_events() -> list[dict]:
    """
    Собирает список мероприятий с сайта RussiaRunning.

    Функция постранично получает данные через API,
    извлекает информацию о мероприятиях и объединяет
    результаты всех страниц в единый список.

    Returns:
        list[dict]:
            Список мероприятий в виде словарей.
    """
    all_events = []

    page_size = 12
    skip = 0

    while True:
        page_data = get_event_page(
            skip=skip,
            page_size=page_size,
            date_from="2026-05-23T00:00:00.000Z",
            date_to="2026-05-23T23:59:00.000Z",
        )

        events = parse_event_page(page_data)

        all_events.extend(events)

        total_count = page_data["totalCount"]

        if len(all_events) >= total_count:
            break

        skip += page_size

    return all_events


if __name__ == "__main__":
    main()

    