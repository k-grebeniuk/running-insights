from playwright.sync_api import sync_playwright


def create_browser() -> tuple:
    """
    Создает экземпляр браузера Chromium.

    Returns:
        tuple:
            playwright,
            browser,
            page
    """

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    return playwright, browser, page