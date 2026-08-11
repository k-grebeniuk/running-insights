EXCLUDED_EVENT_CODES = {
    "DetskiyzabegBEGIGEROY2026",
    "BlagotvoritelnyypolumarafonBEGIGEROY2026",
}


def filter_events(events: list[dict]) -> list[dict]:
    """
    Исключает из списка мероприятия, которые не должны участвовать
    в дальнейшем анализе.

    Фильтрация выполняется по коду мероприятия (event code),
    находящемуся в списке исключений.

    Args:
        events (list[dict]):
            Список мероприятий, полученный после парсинга API.

    Returns:
        list[dict]:
            Отфильтрованный список мероприятий.
    """

    return [
        event
        for event in events
        if event["code"] not in EXCLUDED_EVENT_CODES
    ]