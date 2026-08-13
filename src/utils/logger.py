import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "running-insights.log"


def get_logger(name: str) -> logging.Logger:
    """
    Создаёт и настраивает логгер проекта.

    Args:
        name:
            Имя логгера, обычно __name__ текущего модуля.

    Returns:
        Настроенный экземпляр logging.Logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

