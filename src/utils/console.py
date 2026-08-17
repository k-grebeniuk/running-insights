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
    Отображает текущий прогресс выполнения операции.

    Args:
        label (str):
            Описание выполняемой операции.

        current (int):
            Текущее количество обработанных элементов.

        total (int):
            Общее количество элементов.

    Returns:
        None:
            Функция обновляет текущую строку консоли
            и ничего не возвращает.
    """

    print(
        f"\r{label}: {current:>5} / {total}",
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


def show_total_progress(
    current: int,
    total: int,
) -> None:
    """
    Отображает общий прогресс сбора результатов за текущий день.

    Args:
        current (int):
            Количество уже собранных результатов.

        total (int):
            Общее количество результатов, полученное
            предварительным подсчётом.

    Returns:
        None:
            Функция выводит информацию в консоль
            и ничего не возвращает.
    """

    print(
        f"Всего результатов: {current:>7} / {total:<7}",
    )