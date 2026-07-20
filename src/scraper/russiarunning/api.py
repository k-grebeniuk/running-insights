from typing import Any

import requests


# Эндпоинты API
# базовый адрес:
BASE_URL = "https://results.russiarunning.com/api"
# вернуть список мероприятий:
EVENTS_LIST_URL = f"{BASE_URL}/events/list"
# вернуть подробную информацию об одном мероприятии:
EVENTS_GET_URL = f"{BASE_URL}/events/get"


def get_event_page(
    skip: int,
    page_size: int,
    date_from: str,
    date_to: str,
) -> dict[str, Any]:
    """
    Получает одну страницу списка мероприятий RussiaRunning.

    Args:
        skip: Количество мероприятий, которое необходимо пропустить.
        page_size: Количество мероприятий, которое необходимо получить.
        date_from: Начало периода поиска (ISO 8601).
        date_to: Конец периода поиска (ISO 8601).

    Returns:
        JSON-ответ API в виде словаря.
    """

    payload = {
        "filter": {
            "place": None,
            "dateFrom": date_from,
            "dateTo": date_to,
        },
        "page": {
            "skip": skip,
            "take": page_size,
        },
        "language": "ru",
    }

    response = requests.post(
        EVENTS_LIST_URL,
        json=payload,
    )

    response.raise_for_status()

    return response.json()


def get_event(event_code: str,) -> dict[str, Any]:
    """
    Получает подробную информацию о мероприятии RussiaRunning.

    Args:
        event_code (str):
            Код мероприятия.

    Returns:
        dict[str, Any]:
            Ответ API в виде словаря.
    """

    payload = {"eventCode": event_code, "language": "ru",}
    response = requests.post(EVENTS_GET_URL, json=payload,)

    response.raise_for_status()

    return response.json()