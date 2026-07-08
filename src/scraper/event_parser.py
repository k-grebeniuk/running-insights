from playwright.sync_api import Page


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