from pathlib import Path

from src.scraper.collector import (
    collect_events,
    collect_races,
    collect_participants,
)
from src.scraper.event_filter import filter_events
from src.storage.json_writer import save_json


def main():
    event_date = "2026-05-23"

    project_root = Path(__file__).resolve().parents[2]

    year_dir = (
        project_root
        / "data"
        / "raw"
        / str(event_date)
    )

    events_path = year_dir / "events.json"
    races_path = year_dir / "races.json"
    participants_dir = year_dir / "participants"

    date_from = f"{event_date}T00:00:00.000Z"
    date_to = f"{event_date}T23:59:00.000Z"

    # 1. Собираем мероприятия
    events = collect_events(
        date_from=date_from,
        date_to=date_to,
    )

    # 2. Фильтруем мероприятия
    filtered_events = filter_events(events)

    # 3. Сохраняем мероприятия
    save_json(
        filtered_events,
        events_path,
    )

    # 4. Собираем дистанции
    races = collect_races(filtered_events)

    # 5. Сохраняем дистанции
    save_json(
        races,
        races_path,
    )

    # 6. Собираем участников
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

            # убираем неиспользуемые данные об участниках (опционально):
            participant.pop("stageResults", None)
            participant.pop("video", None)

        save_json(
            participants,
            participants_dir
            / f'{race["event_code"]}_{race["race_id"]}.json',
        )

        print("\n",
            f"✓ {race['event_title']} — {race['race_name']}: "
            f"{len(participants)} участников",
            "\n"
        )


if __name__ == "__main__":
    main()