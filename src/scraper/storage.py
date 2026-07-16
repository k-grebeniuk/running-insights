import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

PARTICIPANTS_DIR = DATA_DIR / "participants"

EVENTS_FILE = DATA_DIR / "events.csv"


def save_participants(participants: list[dict], event_id: str,) -> None:
    """
    Сохраняет результаты участников мероприятия в CSV-файл.
    Args:
        participants (list[dict]):
            Список участников, полученный парсером.

        event_id (str):
            Идентификатор мероприятия.

    Returns:
        None
    """

    if not participants:
        print("Нет данных для сохранения.")
        return

    PARTICIPANTS_DIR.mkdir(parents=True, exist_ok=True,)

    file_path = PARTICIPANTS_DIR / f"{event_id}.csv"
    file_exists = file_path.exists()
    fieldnames = participants[0].keys()

    with open(file_path, "a", newline="", encoding="utf-8-sig",) as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames,)

        if not file_exists:
            writer.writeheader()

        writer.writerows(participants)



def save_events(events: list[dict]) -> None:
    """
    Сохраняет информацию о мероприятиях в CSV-файл.

    Если файл не существует, создаёт его и записывает заголовки.
    Если файл существует, добавляет новые строки.

    Args:
        events (list[dict]):
            Список мероприятий для сохранения.

    Returns:
        None:
            Функция сохраняет данные в файл и ничего не возвращает.
    """

    if not events:
        print("Нет данных для сохранения.")
        return

    DATA_DIR.mkdir(exist_ok=True)

    file_exists = EVENTS_FILE.exists()
    fieldnames = events[0].keys()

    with EVENTS_FILE.open("a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerows(events)


