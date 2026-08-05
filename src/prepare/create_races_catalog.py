from pathlib import Path

import pandas as pd


RAW_RACES_PATH = Path("data/raw/russiarunning/races.json")
OUTPUT_PATH = Path("data/processed/raw_race_catalog.csv")


def build_raw_race_catalog() -> None:
    """
    Создает черновик каталога дистанций из сырых данных.

    Каталог содержит уникальные комбинации race_name и distance
    и используется для последующей ручной нормализации.
    """

    races = pd.read_json(RAW_RACES_PATH)

    race_catalog = (
        races.assign(distance=races["distance"].round(1))
        [["race_name", "distance"]]
        .drop_duplicates()
        .sort_values(["distance", "race_name"])
        .reset_index(drop=True)
    )

    race_catalog.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8",
    )


if __name__ == "__main__":
    build_raw_race_catalog()