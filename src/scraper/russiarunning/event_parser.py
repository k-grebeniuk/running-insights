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