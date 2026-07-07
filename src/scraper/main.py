from browser import create_browser
from paginator import (
    get_last_page,
    go_to_page,
    get_current_page,
)
from parser import parse_participants
from storage import save_participants



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


        for page_num in range(1, last_page + 1):

            print(f"Парсим страницу {page_num}/{last_page}")

            # переходим на нужную страницу
            go_to_page(page,page_num)

            # проверяем, что реально перешли
            current = get_current_page(page)
            print(f"Текущая страница: {current}")

            # извлекаем участников
            participants = parse_participants(page)
            print(f"Получено участников: {len(participants)}")

            # сохраняем в CSV
            save_participants(participants,'event_id')


    finally:
        browser.close()
        playwright.stop()


if __name__ == "__main__":
    main()