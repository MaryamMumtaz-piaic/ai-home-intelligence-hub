import json
import threading
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STORE_DIR = DATA_DIR / "store"
STORE_DIR.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()


def _store_path(collection: str) -> Path:
    return STORE_DIR / f"{collection}.json"


def read_collection(collection: str) -> list[dict[str, Any]]:
    path = _store_path(collection)
    if not path.exists():
        return []
    with _lock:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []


def write_collection(collection: str, items: list[dict[str, Any]]) -> None:
    path = _store_path(collection)
    with _lock:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)


def append_reference_log(filename: str, entry: dict[str, Any]) -> None:
    """Append an entry to a reference JSON file under app/data (e.g. feedback.json, contacts.json)."""
    path = DATA_DIR / filename
    with _lock:
        items: list[dict[str, Any]] = []
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    items = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                items = []
        items.append(entry)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)


def load_reference_data(filename: str) -> Any:
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
