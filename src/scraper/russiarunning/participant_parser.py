from typing import Any


def parse_participants_page(
    page_data: dict[str, Any],
) -> list[dict]:
    """
    Извлекает участников из одной страницы ответа API.

    Args:
        page_data:
            JSON-ответ API.

    Returns:
        list[dict]:
            Список участников.
    """

    return page_data["results"]