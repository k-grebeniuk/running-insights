from browser import create_browser
from paginator import get_last_page
from paginator import go_to_page
from paginator import get_current_page


URL = "https://heroleague.ru/results/zabeg2026_554234"

playwright, browser, page = create_browser()


try:
    page.goto(URL)
    page.wait_for_selector("nav[aria-label='Countries Pagination']")

    page.wait_for_timeout(2000)

    last_page = get_last_page(page)


    print("Последняя страница:", last_page)

    for page_num in range(1, last_page + 1):
        go_to_page(page, page_num)
        current = get_current_page(page)

        print("Активная страница:", current)


finally:
    browser.close()
    playwright.stop()