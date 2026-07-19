import json
from pathlib import Path


def save_json(
    data: list[dict],
    file_path: Path,
) -> None:
    """
    Сохраняет список словарей в JSON-файл.

    Если директория для сохранения отсутствует,
    она создаётся автоматически.
    Существующий файл перезаписывается актуальными данными.

    Args:
        data (list[dict]):
            Данные для сохранения.

        file_path (Path):
            Полный путь к JSON-файлу.

    Returns:
        None:
            Функция сохраняет данные в файл и ничего не возвращает.
    """

    path = Path(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )