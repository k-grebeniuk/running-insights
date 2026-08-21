EXCLUDED_EVENT_CODES = {
    # 2026
    "DetskiyzabegBEGIGEROY2026",
    "BlagotvoritelnyypolumarafonBEGIGEROY2026",

    # 2025
    "BlagotvoritelnyypolumarafonBEGIGEROY2025",
    "DetskiyzabegBEGIGEROY2025",
    "meleuz2025",

    # 2024
    "runhero",
    "VILipetskiypolumarafon",

    # 2023
    "zabeg23",

    # 2022

    # 2021

    # 2020
    "RunHeroNNovgorod2020",

    # 2019
    "RunHeroNNovgorod2019",

    # 2018
    "4dadd052-162a-4725-8443-8f778a1c6ed0",

    # 2017
    "SpringHalfMarathonOmsk2017",
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