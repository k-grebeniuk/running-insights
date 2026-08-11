from pathlib import Path
import json
import pandas as pd


PARTICIPANTS_DIR = Path(
    "data/raw/russiarunning/participants"
)

OUTPUT_FILE = Path(
    "data/processed/participants_raw.csv"
)


COLUMNS = [
    "participantId",

    "event_id",
    "race_id",

    "disciplineCode",

    "position",
    "number",

    "individualResult",
    "status",

    "fullName",
    "age",
    "gender",
]


def build_participants() -> None:
    """
    Объединяет данные об участниках из отдельных JSON-файлов
    в единую таблицу CSV.

    Для каждого JSON-файла из директории с данными участников
    извлекаются только поля, необходимые для дальнейшего анализа.
    Полученные записи объединяются в один DataFrame и сохраняются
    в виде CSV-файла.

    Args:
        None:
            Функция не принимает аргументов. Пути к исходным и
            выходным данным задаются глобальными константами
            `PARTICIPANTS_DIR` и `OUTPUT_FILE`.

    Returns:
        None:
            Функция сохраняет результат в `OUTPUT_FILE` и не
            возвращает DataFrame.
    """
    participants = []

    for file in PARTICIPANTS_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for participant in data:
            row = {
                column: participant.get(column)
                for column in COLUMNS
            }

            participants.append(row)

    df = pd.DataFrame(participants)

    print("Собрано участников: ", df["participantId"].nunique())
    print("Количество мероприятий: ", df["event_id"].nunique())
    print("Количество дистанций: ", df["race_id"].nunique())

    print(
    f"Processed {len(participants)} participants"
)
    

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )



if __name__ == "__main__":
    build_participants()