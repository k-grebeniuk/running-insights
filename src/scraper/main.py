from browser import create_browser
from paginator import (
    get_last_page,
    go_to_page,
    get_current_page,
)
from parser import parse_participants



URL = "https://heroleague.ru/results/zabeg2026_554234"      #Зеленоградск
#URL = "https://heroleague.ru/results/zabeg2026_498817"      #Санкт-Петербург


def main():
    playwright, browser, page = create_browser()


    try:
        page.goto(URL)
        page.wait_for_selector("nav[aria-label='Countries Pagination']")

        page.wait_for_timeout(2000)
        last_page = get_last_page(page)

        print("Последняя страница:", last_page)

        # Проверяем parser:
        rows = parse_participants(page)
        for row in rows:
            print(row)



        #for page_num in range(1, last_page + 1):
            #go_to_page(page, page_num)
            #current = get_current_page(page)

            #print(f"Обработка страницы {current} из {last_page}")


    finally:
        browser.close()
        playwright.stop()


if __name__ == "__main__":
    main()