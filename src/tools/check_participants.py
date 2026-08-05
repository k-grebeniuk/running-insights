import json
from pathlib import Path


participants_dir = Path("data/raw/russiarunning/participants")
total_participants_count = 0

for path in sorted(participants_dir.glob("*.json")):
    with path.open("r", encoding="utf-8") as f:
        participants = json.load(f)

        participants_count = len(participants)
        total_participants_count += participants_count

    print(f"{path.name}: {participants_count}")

print(f"Всего собрано участников: {total_participants_count}")