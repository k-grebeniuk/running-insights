from playwright.sync_api import sync_playwright
import pandas as pd
import time

URL = "https://heroleague.ru/results/zabeg2026_554234"

all_results = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(URL)

    # ждем загрузку таблицы
    page.wait_for_selector('div[role="row"]')

    time.sleep(3)

    # получаем все строки
    rows = page.locator('div[role="row"]').all()

    print(f"Найдено строк: {len(rows)}")

    for row in rows:

        cells = row.locator('div[role="cell"]').all_inner_texts()

        # пропускаем пустые строки
        if not cells:
            continue

        print(cells)

        all_results.append({
            "bib": cells[0] if len(cells) > 0 else None,
            "name": cells[1] if len(cells) > 1 else None,
            "surname": cells[2] if len(cells) > 2 else None,
            "category": cells[3] if len(cells) > 3 else None,
            "time_clean": cells[4] if len(cells) > 4 else None,
            "place_category": cells[5] if len(cells) > 5 else None,
            "status": cells[6] if len(cells) > 6 else None,
        })

    browser.close()

df = pd.DataFrame(all_results)

print(df.head())

df.to_csv("data//zabeg_results.csv", index=False)

print("CSV сохранен")