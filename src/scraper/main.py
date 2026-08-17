from pathlib import Path

from src.scraper.collector import (
    collect_events,
    collect_races,
    collect_participants,
    collect_relay_results,
    collect_total_results_count
)
from src.scraper.event_filter import filter_events
from src.storage.json_writer import save_json
from src.utils.logger import get_logger
from src.utils.console import (
    show_collection_end,
    show_collection_start,
    show_event,
    show_race,
)


logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EVENT_DATES = (
    "2026-05-23",
    "2025-05-24",
    "2024-05-19",
    "2023-06-04",
    "2022-05-22",
    "2021-05-30",
    "2020-08-02",
    "2019-05-19",
    "2018-05-20",
    "2017-05-21"
)


def main():

    result_counts = []
    for event_date in EVENT_DATES:

        logger.info("Начало сбора данных: %s", event_date)
        show_collection_start(event_date)

        raw_dir = (
            PROJECT_ROOT
            / "data"
            / "raw"
            / event_date
        )

        processed_dir = (
            PROJECT_ROOT
            / "data"
            / "processed"
            / event_date
        )

        events_path = raw_dir / "events.json"
        races_path = processed_dir / "races.json"
        participants_dir = raw_dir / "participants"
        relay_dir = raw_dir / "relay"

        date_from = f"{event_date}T00:00:00.000Z"
        date_to = f"{event_date}T23:59:00.000Z"

        # собираем мероприятия
        events = collect_events(
            date_from=date_from,
            date_to=date_to,
        )

        # фильтруем мероприятия
        filtered_events = filter_events(events)

        # сохраняем мероприятия
        save_json(
            filtered_events,
            events_path,
        )

        # собираем дистанции
        races = collect_races(filtered_events)

        # сохраняем дистанции
        save_json(
            races,
            races_path,
        )

        # предварительно считаем общее количество результатов
        total_results_count = collect_total_results_count(races)
        result_counts.append(f"{event_date} ==== {total_results_count:_}")
        print(event_date, '====', total_results_count)

    print('\n', *result_counts, sep='\n')

    '''    # собираем участников
        current_event_id = None

        for race in races:

            if race["event_id"] != current_event_id:
                show_event(race["event_title"])
                current_event_id = race["event_id"]

            show_race(race["race_name"])

            logger.info(
                "Сбор результатов: %s — %s",
                race["event_title"],
                race["race_name"],
            )

            if race["is_relay"]:
                results = collect_relay_results(
                    event_id=race["event_id"],
                    race_id=race["race_id"],
                )

                save_dir = relay_dir

            else:
                results = collect_participants(
                    event_id=race["event_id"],
                    race_id=race["race_id"],
                )

                for participant in results:
                    participant.pop("stageResults", None)
                    participant.pop("video", None)

                save_dir = participants_dir

            for result in results:
                result["event_id"] = race["event_id"]
                result["event_code"] = race["event_code"]
                result["event_title"] = race["event_title"]
                result["race_id"] = race["race_id"]
                result["race_name"] = race["race_name"]

            if results:
                save_json(
                    results,
                    save_dir / (f'{event_date}_{race["event_code"]}_{race["race_id"]}.json'),
                )

            logger.info(
                "Сбор завершён: %s — %s: %d результатов",
                race["event_title"],
                race["race_name"],
                len(results),
            )
            
        show_collection_end()'''

if __name__ == "__main__":
    main()