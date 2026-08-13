def show_collection_start(event_date: str) -> None:
    """
    Отображает начало сбора данных за указанную дату.

    Args:
        event_date (str):
            Дата проведения мероприятий.

    Returns:
        None:
            Функция выводит информацию в консоль
            и ничего не возвращает.
    """

    print()
    print("=" * 60)
    print(f"СБОР ДАННЫХ: {event_date}")
    print("=" * 60)
    print()


def show_event(event_title: str) -> None:
    """
    Отображает название текущего мероприятия.

    Args:
        event_title (str):
            Название мероприятия.

    Returns:
        None:
            Функция выводит информацию в консоль
            и ничего не возвращает.
    """

    print()
    print(event_title)


def show_race(race_name: str) -> None:
    """
    Отображает название текущей дистанции.

    Args:
        race_name (str):
            Название дистанции.

    Returns:
        None:
            Функция выводит информацию в консоль
            и ничего не возвращает.
    """

    print(f"  → {race_name}")


def show_progress(
    label: str,
    current: int,
    total: int,
) -> None:
    """
    Отображает текущий прогресс сбора результатов.

    Args:
        label (str):
            Описание текущей операции.

        current (int):
            Текущее количество собранных результатов.

        total (int):
            Общее количество результатов.

    Returns:
        None:
            Функция выводит информацию в консоль
            и ничего не возвращает.
    """

    print(
        f"\r    {label}: {current:>5} / {total}",
        end="",
        flush=True,
    )


def show_collection_end() -> None:
    """
    Отображает завершение сбора данных.

    Returns:
        None:
            Функция выводит информацию в консоль
            и ничего не возвращает.
    """

    print()
    print()
    print("СБОР ДАННЫХ ЗАВЕРШЁН")
    print()