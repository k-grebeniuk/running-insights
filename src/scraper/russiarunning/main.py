from src.scraper.russiarunning.api import (get_event_page,
                                           get_event,
                                           get_participants_page)
from src.scraper.russiarunning.event_parser import (parse_event_page,
                                                    extract_races)
from src.scraper.russiarunning.event_filter import filter_events
from src.storage.json_writer import save_json

from pathlib import Path
import time


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

        races.extend(event_races)

    save_json(
        races,
        Path("data/raw/russiarunning/races.json"),
    )


    for race in races:
        print(f'Собираю участников: {race["event_title"]} — {race["race_name"]}')
        participants = collect_participants(
            event_id=race["event_id"],
            race_id=race["race_id"],
        )

        for participant in participants:
            participant["event_id"] = race["event_id"]
            participant["event_code"] = race["event_code"]
            participant["event_title"] = race["event_title"]

            participant["race_id"] = race["race_id"]
            participant["race_name"] = race["race_name"]

            #убираем неиспользуемые данные об участниках (опционально):
            participant.pop("stageResults", None)
            participant.pop("video")

        save_json(
            participants,
            Path(f'data/raw/russiarunning/participants/{race["event_code"]}_{race["race_id"]}.json'),
        )

        print("\n",
            f"✓ {race['event_title']} — {race['race_name']}: "
            f"{len(participants)} участников",
            "\n"
        )

def collect_participants(
    event_id: str,
    race_id: str,
) -> list[dict]:
    """
    Собирает всех участников одной дистанции.

    Args:
        event_id: Идентификатор мероприятия.
        race_id: Идентификатор дистанции.

    Returns:
        Список участников дистанции.
    """

    participants = []

    page_size = 50
    skip = 0

    while True:
        page_data = get_participants_page(
            event_id=event_id,
            race_id=race_id,
            skip=skip,
            page_size=page_size,
        )

        participants.extend(page_data["results"])

        total_count = page_data["totalCount"]

        print(
            f"\rСобрано участников: {len(participants):>5} / {total_count}",
            end="",
            flush=True,
        )

        if len(participants) >= total_count:
            break

        skip += page_size

        time.sleep(0.3)

    return participants



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

    