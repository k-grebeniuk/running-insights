from pathlib import Path
import pandas as pd

from src.prepare.create_races_catalog import build_race_catalog


def merge_participant_references(
    participants: pd.DataFrame,
) -> pd.DataFrame:
    """
    Добавляет к данным участников расшифровки статусов и пола.

    Связь со справочниками выполняется по идентификаторам,
    содержащимся в таблице участников: `status` связывается
    с `status_id`, а `gender` — с `gender_id`.

    Args:
        participants (pd.DataFrame):
            Таблица участников, содержащая поля `status` и `gender`.

    Returns:
        pd.DataFrame:
            Таблица участников, дополненная данными из справочников
            статусов и пола.
    """

    status_types = pd.read_csv(
        "data/reference/status_types.csv"
    )

    gender_types = pd.read_csv(
        "data/reference/gender_types.csv"
    )

    dataset = (
        participants
        .merge(
            status_types,
            left_on="status",
            right_on="status_id",
            how="left"
        )
        .merge(
            gender_types,
            left_on="gender",
            right_on="gender_id",
            how="left"
        )
    )

    return dataset


def merge_events(
    participants: pd.DataFrame,
) -> pd.DataFrame:
    """
    Добавляет к данным участников информацию о мероприятиях.

    Участник связывается с мероприятием по полю `event_id`
    из таблицы участников и полю `id` из `events.json`.

    Args:
        participants (pd.DataFrame):
            Таблица участников, содержащая поле `event_id`.

    Returns:
        pd.DataFrame:
            Таблица участников, дополненная данными о мероприятии:
            названием, местом проведения, датой начала и датой окончания.
    """

    events = pd.read_json(
        "data/raw/russiarunning/events.json"
    )

    dataset = participants.merge(
        events[
            [
                "id",
                "title",
                "place",
            ]
        ],
        left_on="event_id",
        right_on="id",
        how="left",
    )

    return dataset


def merge_race_catalog(
    races: pd.DataFrame,
    race_catalog: pd.DataFrame,
) -> pd.DataFrame:
    """
    Добавляет к данным о забегах информацию из каталога.

    Связывает записи по названию забега и дистанции (`race_name`, `distance`) 
    и добавляет к данным из `races` классификацию дистанции и типа забега,
    полученную из нормализованного каталога.

    Args:
        races (pd.DataFrame):
            Данные о забегах, полученные из `races.json`.

        race_catalog (pd.DataFrame):
            Нормализованный и обогащенный каталог забегов.

    Returns:
        pd.DataFrame:
            Данные о забегах, дополненные информацией из каталога.
    """

    dataset = races.merge(
        race_catalog,
        on=["race_name", "distance"],
        how="left",
        suffixes=("_race", "_catalog"),
    )

    return dataset


def merge_races(
    participants: pd.DataFrame,
    races: pd.DataFrame,
) -> pd.DataFrame:
    """
    Добавляет к данным участников информацию о дистанциях,
    в которых они принимали участие.

    Args:
        participants (pd.DataFrame):
            Данные участников мероприятий. Должны содержать
            столбец `race_id`.

        races (pd.DataFrame):
            Каталог дистанций мероприятий. Должен содержать
            уникальный `race_id` и связанные с ним характеристики
            дистанции и мероприятия.

    Returns:
        pd.DataFrame:
            Датасет участников, дополненный информацией о
            соответствующей дистанции и мероприятии.
    """

    return participants.merge(
        races,
        on="race_id",
        how="left",
    )


def select_and_rename_columns(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    """
    Выбирает колонки, необходимые для итогового аналитического
    датасета, и приводит их названия к единому стилю.

    Args:
        dataset (pd.DataFrame):
            Полный датасет участников после объединения
            со справочниками, мероприятиями и дистанциями.

    Returns:
        pd.DataFrame:
            Датасет с выбранными колонками и нормализованными
            названиями.
    """

    columns = {
        "participantId": "participant_id",
        "event_id_x": "event_id",
        "race_id": "race_id",
        "position": "position",
        "number": "bib_number",
        "individualResult": "finish_time",
        "fullName": "full_name",
        "age": "age",
        "status_code": "status_code",
        "status_name": "status_name",
        "gender_code": "gender_code",
        "gender_name": "gender_name",
        "place": "event_place",
        "race_name": "race_name",
        "event_code": "event_code",
        "event_title": "event_title",
        "distance_km": "distance_km",
        "distance_name": "distance_name",
        "race_type_code": "race_type_code",
        "race_type_name": "race_type_name",
    }

    return dataset[list(columns)].rename(columns=columns)



def main() -> None:
    """
    Формирует итоговый датасет участников.

    Функция загружает подготовленные данные об участниках и забегах,
    последовательно обогащает их справочниками и каталогом забегов,
    а затем возвращает управление после выполнения полного
    процесса трансформации.

    Args:
        None.

    Returns:
        None:
            Результат трансформации формируется в DataFrame
            и на текущем этапе выводится для проверки.
    """

    participants = pd.read_csv("data/processed/participants_raw.csv")

    races = pd.read_json("data/raw/russiarunning/races.json")

    # Добавляем расшифровку статуса и пола:
    dataset = merge_participant_references(participants)

    # Добавляем информацию о мероприятии:
    dataset = merge_events(dataset)

    # Создаем полноценный каталог забегов:
    race_catalog = build_race_catalog()

    # Связываем забеги из races.json с каталогом:
    final_race_catalog = merge_race_catalog(
        races,
        race_catalog,
    )

    # Добавляем информацию об дистанциях для каждого из участников:
    dataset = merge_races(dataset, final_race_catalog)

    # Выбираем и переименовываем колонки перед сохранением:
    dataset = select_and_rename_columns(dataset)

    dataset.to_csv(
    "data/processed/final_participants.csv",
    index=False,
    encoding="utf-8",)


if __name__ == "__main__":
    main()

