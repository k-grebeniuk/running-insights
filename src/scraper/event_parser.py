from playwright.sync_api import Page, Locator


def select_event_filter(page: Page) -> None:
    """
    Выбирает фильтр "Забег" в списке мероприятий.
    Args:
        page (Page):
            Открытая страница Playwright.
    Returns:
        None:
            Функция изменяет состояние страницы.
    """

    #открываем селектор - выпадающий список
    selector = page.locator(".select-activity-container .select-activity__control")
    selector.click()
    page.wait_for_timeout(1000)

    #выбираем "Забег"
    option = page.get_by_role("option", name="Забег", exact=True)
    option.click()
    page.wait_for_timeout(3000)


def parse_events(page: Page) -> list[dict]:
    """
    Извлекает список мероприятий со страницы результатов.
    Args:
        page (Page):
            Открытая страница Playwright.
    Returns:
        list[dict]:
            Список мероприятий.
    """

    cards = page.locator("li._item_18tis_50")
    events = []

    for i in range(cards.count()):

        card = cards.nth(i)
        raw_url = card.locator("a").get_attribute("href")

        event = {
            "date": card.locator("span").first.inner_text(),
            "city": card.locator("b").inner_text(),
            "name": card.locator("p").inner_text(),
            "url": normalize_url(raw_url)
        }
        events.append(event)

    return events


def normalize_url(url: str | None) -> str | None:
    """
    Преобразует относительные ссылки в абсолютные.
    """

    if url is None:
        return None

    if url.startswith("/"):
        return f"https://heroleague.ru{url}"

    return url



def select_distance(page: Page, site_distance: str) -> bool:
    """
    ОПИСАНИЕ!!!
    """

    locator = page.locator(f"label[for='{site_distance}_filter']")

    if locator.count() == 0:
        return False

    locator.click()
    page.wait_for_timeout(300)

    return True


def normalize_distance(distance: str) -> str:
    """
    Приводит название дистанции к единому виду.

    Args:
        distance (str):
            Название дистанции с сайта.

    Returns:
        str:
            Нормализованное название дистанции.
    """

    distance = distance.lower()
    distance = distance.replace(".", ",")
    distance = distance.replace(" ", "")
    distance = distance.replace("km", "км")

    if distance.startswith("1км"):
        return "1 км"

    if distance.startswith("5км"):
        return "5 км"

    if distance.startswith("10км"):
        return "10 км"

    if distance.startswith("21"):
        return "21 км"

    return distance



def get_distances(page: Page) -> dict[str, str]:
    """
    Извлекает список дистанций мероприятия.

    Args:
        page (Page):
            Страница результатов соревнования.

    Returns:
        dict[str, str]:
            Словарь вида:

            {
                "1 км": "1 km",
                "5 км": "5км",
                "10 км": "10 km",
                "21 км": "21.1 km"
            }

        Ключ — внутреннее название дистанции.
        Значение — текст кнопки на сайте.
    """

    distances = {}

    labels = page.locator("label[for$='_filter']")

    for i in range(labels.count()):

        site_name = labels.nth(i).inner_text().strip()

        internal_name = normalize_distance(site_name)

        distances[internal_name] = site_name

    return distances