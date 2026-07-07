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


def go_to_page(page, page_num):
    print("Переходим на:", page_num)

    button = page.get_by_role("link", name=str(page_num), exact=True)

    while button.count() == 0:
        print("Страница не видна, нажимаем Next")

        page.get_by_role("link", name="Next").click()
        page.wait_for_timeout(1000)

        button = page.get_by_role("link",name=str(page_num),exact=True)

    button.click()
    page.wait_for_timeout(1000)


def get_current_page(page):
    active = page.locator("._pageItemActive_5vuzn_46").inner_text()

    return active