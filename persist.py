import os
import json
import threading

PERSIST_PATH = os.path.join(os.path.dirname(__file__), 'data', 'persist.json')
_lock = threading.Lock()


def _write(data):
    os.makedirs(os.path.dirname(PERSIST_PATH), exist_ok=True)
    tmp = PERSIST_PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, default=str)
    os.replace(tmp, PERSIST_PATH)


def _read():
    try:
        with open(PERSIST_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save(data: dict) -> None:
    with _lock:
        _write(data)


def load() -> dict | None:
    with _lock:
        return _read()
