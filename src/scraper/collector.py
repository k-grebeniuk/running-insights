import time
import requests

from src.utils.logger import get_logger
from src.scraper.api import (
    get_event_page,
    get_event,
    get_participants_page,
    get_relay_page,
)
from src.scraper.event_parser import (
    parse_event_page,
    extract_races,
)
from src.utils.console import (
    show_progress,
    show_race,
    show_event
)

logger = get_logger(__name__)


def collect_events(
    date_from: str,
    date_to: str,
) -> list[dict]:
    """
    Собирает все мероприятия за указанный период.

    Args:
        date_from: Начальная дата периода в ISO-формате.
        date_to: Конечная дата периода в ISO-формате.

    Returns:
        Список мероприятий.
    """
    all_events = []

    page_size = 12
    skip = 0

    while True:
        page_data = get_event_page(
            skip=skip,
            page_size=page_size,
            date_from=date_from,
            date_to=date_to,
        )

        events = parse_event_page(page_data)
        all_events.extend(events)

        total_count = page_data["totalCount"]

        if len(all_events) >= total_count:
            break

        skip += page_size

    return all_events



def collect_races(events: list[dict]) -> list[dict]:
    """
    Собирает все дистанции для переданных мероприятий.

    Args:
        events: Список мероприятий.

    Returns:
        Список дистанций с информацией о мероприятии.
    """
    races = []

    for event in events:

        # Получаем подробную страницу мероприятия
        event_data = get_event(event["code"])

        # Из неё извлекаем дистанции
        event_races = extract_races(event_data)

        # Добавляем к каждой дистанции информацию о мероприятии
        for race in event_races:
            race["event_id"] = event["id"]
            race["event_code"] = event["code"]
            race["event_title"] = event["title"]
            race["event_place"] = event["place"]
            race["event_address"] = event["address"]

        races.extend(event_races)

    return races



def collect_participants(
    event_id: str,
    race_id: str,
    race_name: str,
):
    """
    Собирает всех участников одной дистанции.

    Если для дистанции отсутствуют результаты,
    возвращает пустой список.

    Args:
        event_id:
            Идентификатор мероприятия.

        race_id:
            Идентификатор дистанции.

        race_name:
            Название дистанции для отображения
            прогресса сбора в консоли.

    Returns:
        Список участников дистанции.
        Пустой список, если результаты отсутствуют.
    """

    participants = []

    page_size = 50
    skip = 0

    while True:

        try:
            page_data = get_participants_page(
                event_id=event_id,
                race_id=race_id,
                skip=skip,
                page_size=page_size,
            )

        except requests.HTTPError as error:

            if error.response is not None and error.response.status_code == 404:
                return []

            raise

        participants.extend(page_data["results"])

        total_count = page_data["totalCount"]

        show_progress(
            f"→ {race_name} | Собрано",
            len(participants),
            total_count,
        )

        if len(participants) >= total_count:
            break

        skip += page_size

        time.sleep(0.3)

    print()

    return participants


def collect_relay_results(
    event_id: str,
    race_id: str,
) -> list[dict]:
    """
    Собирает все результаты эстафеты одной дистанции.

    Args:
        event_id:
            Идентификатор мероприятия.

        race_id:
            Идентификатор дистанции.

    Returns:
        Список результатов эстафеты.
    """

    relay_results = []

    page_size = 50
    skip = 0

    while True:
        page_data = get_relay_page(
            event_id=event_id,
            race_id=race_id,
            skip=skip,
            page_size=page_size,
        )

        results = page_data["results"]

        relay_results.extend(results)

        total_count = page_data["totalCount"]

        show_progress(
            label="Собрано команд",
            current=len(relay_results),
            total=total_count,
        )

        if len(relay_results) >= total_count:
            break

        skip += page_size

        time.sleep(0.3)

    print()

    return relay_results


def collect_total_results_count(races: list[dict]) -> int:
    """
    Получает общее количество результатов по всем дистанциям.

    Дистанции без результатов пропускаются.

    Args:
        races:
            Список дистанций мероприятий.

    Returns:
        Общее количество результатов.
    """

    total_results_count = 0

    for race in races:

        print(f'Проверяю: {race["event_title"]} — {race["race_name"]}')
        try:
            if race["is_relay"]:
                page_data = get_relay_page(
                    event_id=race["event_id"],
                    race_id=race["race_id"],
                    skip=0,
                    page_size=1,
                )
            else:
                page_data = get_participants_page(
                    event_id=race["event_id"],
                    race_id=race["race_id"],
                    skip=0,
                    page_size=1,
                )

        except requests.HTTPError as error:

            if error.response is not None and error.response.status_code == 404:
                logger.warning(
                    "Нет результатов: %s — %s",
                    race["event_title"],
                    race["race_name"],
                )
                continue

            raise

        total_results_count += page_data["totalCount"]

    return total_results_count