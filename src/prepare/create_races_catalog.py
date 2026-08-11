from pathlib import Path

import pandas as pd


RAW_RACES_PATH = Path(
    "data/raw/races.json"
)

RAW_CATALOG_PATH = Path(
    "data/processed/raw_race_catalog.csv"
)

RACE_CATALOG_PATH = Path(
    "data/reference/races_catalog.csv"
)

RACE_TYPES_PATH = Path(
    "data/reference/race_types.csv"
)

DISTANCE_TYPES_PATH = Path(
    "data/reference/distance_types.csv"
)


def build_raw_race_catalog() -> None:
    """
    Создает черновой каталог забегов из сырых данных RussiaRunning.

    Функция извлекает из `races.json` названия забегов и исходные
    значения дистанций, удаляет дубликаты и сортирует записи.

    Полученный каталог используется как основа для последующей
    ручной нормализации названий и классификации забегов.

    Args:
        None.

    Returns:
        None:
            Результат сохраняется в CSV-файл
            `data/processed/raw_race_catalog.csv`.
    """

    races = pd.read_json(RAW_RACES_PATH)

    race_catalog = (
        races[["race_name", "distance"]]
        .drop_duplicates()
        .sort_values(["distance", "race_name"])
        .reset_index(drop=True)
    )

    race_catalog.to_csv(
        RAW_CATALOG_PATH,
        index=False,
        encoding="utf-8",
    )


def build_race_catalog() -> pd.DataFrame:
    """
    Формирует расширенный каталог забегов на основе
    вручную нормализованного справочника.

    Функция загружает `races_catalog.csv`, содержащий вручную
    определенные идентификаторы дистанций и типов забегов, и
    дополняет его данными из справочников `distance_types.csv`
    и `race_types.csv`.

    Полученный DataFrame содержит как исходные данные каталога,
    так и расшифровки идентификаторов дистанций и типов забегов.

    Args:
        None.

    Returns:
        pd.DataFrame:
            Расширенный каталог забегов с данными о дистанциях
            и типах забегов.
    """

    race_catalog = pd.read_csv(
        RACE_CATALOG_PATH
    )

    race_types = pd.read_csv(
        RACE_TYPES_PATH
    )

    distance_types = pd.read_csv(
        DISTANCE_TYPES_PATH
    )

    race_catalog = (
        race_catalog
        .merge(
            distance_types,
            on="distance_id",
            how="left",
        )
        .merge(
            race_types,
            on="race_type_id",
            how="left",
        )
    )

    return race_catalog


if __name__ == "__main__":
    build_raw_race_catalog()
    races = build_race_catalog()
    print(races)