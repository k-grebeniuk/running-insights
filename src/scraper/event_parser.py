from typing import Any


def parse_event_page(page_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Извлекает список мероприятий из ответа API.

    Args:
        page_data: JSON-ответ API со страницей мероприятий.

    Returns:
        Список мероприятий.
    """

    return page_data["list"]


def extract_races(event: dict) -> list[dict]:
    """
    Извлекает информацию о дистанциях мероприятия.

    Args:
        event:
            Данные одного мероприятия,
            полученные из API.

    Returns:
        Список дистанций с идентификаторами,
        названием и длиной.
    """

    return [
        {
            "race_id": race["id"],
            "race_name": race["name"],
            "distance": race["distance"],
            "is_complex": race["isComplex"],
            "is_relay": race["isRelay"],
        }
        for race in event["races"]
]