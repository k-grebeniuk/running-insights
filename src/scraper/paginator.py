from playwright.sync_api import Page


def get_last_page(page: Page) -> int:
    """
    Определяет номер последней страницы пагинации.

    Args:
        page (Page):
            Открытая страница результатов Playwright.

    Returns:
        int:
            Номер последней страницы.
    """

    links = page.locator("nav[aria-label='Countries Pagination'] a").all_inner_texts()
    pages = [int(x) for x in links if x.isdigit()]

    return max(pages)


def go_to_page(page: Page, page_num: int) -> None:
    """
    Переходит на указанную страницу пагинации.

    Если нужная страница не отображается в текущем окне пагинации,
    функция нажимает кнопку Next, пока нужная страница не станет доступна.

    Args:
        page (Page):
            Открытая страница Playwright.

        page_num (int):
            Номер страницы, на которую необходимо перейти.

    Returns:
        None:
            Функция только выполняет переход и ничего не возвращает.
    """

    print("Переходим на:", page_num)

    button = page.get_by_role("link", name=str(page_num), exact=True)

    while button.count() == 0:
        print("Страница не видна, нажимаем Next")

        page.get_by_role("link", name="Next").click()
        page.wait_for_timeout(300)

        button = page.get_by_role("link",name=str(page_num),exact=True)

    button.click()
    page.wait_for_timeout(1000)


def get_current_page(page: Page) -> str:
    """
    Получает номер текущей активной страницы пагинации.
    Args:
        page (Page):
            Открытая страница Playwright.

    Returns:
        str:
            Номер активной страницы.
    """

    active_page = page.locator(
        "nav[aria-label='Countries Pagination'] [class*='_pageItemActive_']"
    ).inner_text()

    return active_page