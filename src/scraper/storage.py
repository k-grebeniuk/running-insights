import csv
from pathlib import Path


DATA_DIR = Path("data")
PARTICIPANTS_FILE = DATA_DIR / "participants.csv"
EVENTS_FILE = DATA_DIR / "events.csv"


def save_participants(participants: list[dict]) -> None:
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

    DATA_DIR.mkdir(exist_ok=True)

    file_exists = EVENTS_FILE.exists()
    fieldnames = participants[0].keys()

    with PARTICIPANTS_FILE.open("a", newline="", encoding="utf-8-sig",) as file:

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


