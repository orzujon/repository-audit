import json
from pathlib import Path


SNAPSHOT_FILE = Path("branch_protection_snapshot.json")


def save_snapshot(snapshot_data):
    with SNAPSHOT_FILE.open("w", encoding="utf-8") as file:
        json.dump(snapshot_data, file, indent=2)

    print(f"Snapshot saved to {SNAPSHOT_FILE}")


def load_snapshot():
    if not SNAPSHOT_FILE.exists():
        raise FileNotFoundError("Snapshot file not found. Run fix mode first.")

    with SNAPSHOT_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)