import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_CANDIDATES = [
    PROJECT_ROOT / "data" / "assignment_buddy_dataset.csv",
    PROJECT_ROOT / "Chatbox_CSC649_GroupAssignment" / "data" / "assignment_buddy_dataset.csv",
]


def load_dataset_context() -> str:
    for path in DATASET_CANDIDATES:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8-sig") as file:
                    rows = list(csv.DictReader(file))
                entries = []
                for row in rows:
                    values = [v.strip() for v in row.values() if v and v.strip()]
                    if len(values) >= 2:
                        entries.append(f"Q: {values[0]}\nA: {values[1]}")
                return "\n\n".join(entries)
            except Exception:
                return ""
    return ""