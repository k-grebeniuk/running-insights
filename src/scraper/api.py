from typing import Any

import logging
import requests


logger = logging.getLogger(__name__)

# Эндпоинты API
# базовый адрес:
BASE_URL = "https://results.russiarunning.com/api"
# вернуть список мероприятий:
EVENTS_LIST_URL = f"{BASE_URL}/events/list"
# вернуть подробную информацию об одном мероприятии:
EVENTS_GET_URL = f"{BASE_URL}/events/get"
# вернуть информацию об индивидуальных результатах
INDIVIDUAL_RESULTS_GET_URL = f"{BASE_URL}/results/individual/get"
# вернуть информацию о результатах эстафеты
RELAY_RESULTS_GET_URL = f"{BASE_URL}/results/relay/get"


REQUEST_TIMEOUT = 30

session = requests.Session()

session.headers.update({
    "User-Agent": (
        "running-insights/1.0 "
        "(https://github.com/k-grebeniuk/running-insights)"
    )
})


def _post(
    url: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """
    Выполняет POST-запрос к API RussiaRunning.

    При успешном выполнении возвращает JSON-ответ API.
    В случае ошибки записывает информацию в лог
    и повторно вызывает исключение.

    Args:
        url (str):
            URL эндпоинта API.

        payload (dict[str, Any]):
            Данные, передаваемые в теле POST-запроса.

    Returns:
        dict[str, Any]:
            JSON-ответ API в виде словаря.

    Raises:
        requests.Timeout:
            Если время ожидания ответа API истекло.

        requests.ConnectionError:
            Если не удалось установить соединение с API.

        requests.HTTPError:
            Если API вернул HTTP-ошибку.
    """

    try:
        response = session.post(
            url,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    except requests.Timeout:
        logger.error(
            "Таймаут API-запроса: %s",
            url,
        )
        raise

    except requests.ConnectionError:
        logger.error(
            "Ошибка соединения с API: %s",
            url,
        )
        raise

    except requests.HTTPError as error:
        status_code = (
            error.response.status_code
            if error.response is not None
            else "unknown"
        )

        logger.error(
            "Ошибка API: HTTP %s — %s",
            status_code,
            url,
        )
        raise



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

    return _post(
        EVENTS_LIST_URL,
        payload,
    )


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

    return _post(
        EVENTS_GET_URL,
        payload,
    )


def get_participants_page(
    event_id: str,
    race_id: str,
    skip: int,
    page_size: int,
) -> dict[str, Any]:
    """
    Получает одну страницу индивидуальных результатов выбранной дистанции.

    Args:
        event_id:
            Идентификатор мероприятия.

        race_id:
            Идентификатор дистанции.

        skip:
            Количество участников, которое необходимо пропустить.

        page_size:
            Количество участников, которое необходимо получить.

    Returns:
        dict[str, Any]:
            JSON-ответ API в виде словаря.
    """
    payload = {
    "eventId": event_id,
    "raceId": race_id,
    "filter": {},
    "isStagesOn": True,
    "language": "ru",
    "page": {
        "skip": skip,
        "take": page_size,
    },
}
    
    return _post(
        INDIVIDUAL_RESULTS_GET_URL,
        payload,
    )


def get_relay_page(
    event_id: str,
    race_id: str,
    skip: int,
    page_size: int,
) -> dict[str, Any]:
    """
    Получает одну страницу результатов эстафеты.

    Args:
        event_id:
            Идентификатор мероприятия.

        race_id:
            Идентификатор дистанции.

        skip:
            Количество результатов, которое необходимо пропустить.

        page_size:
            Количество результатов, которое необходимо получить.

    Returns:
        dict[str, Any]:
            JSON-ответ API в виде словаря.
    """

    payload = {
        "eventId": event_id,
        "raceId": race_id,
        "filter": {},
        "isStagesOn": True,
        "language": "ru",
        "page": {
            "skip": skip,
            "take": page_size,
        },
    }

    return _post(
        RELAY_RESULTS_GET_URL,
        payload,
    )