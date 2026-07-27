import json
from pathlib import Path

participants_dir = Path("data/raw/russiarunning/participants")

for path in sorted(participants_dir.glob("*.json")):
    with path.open("r", encoding="utf-8") as f:
        participants = json.load(f)

    print(f"{path.name}: {len(participants)}")