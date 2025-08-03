import json
from pathlib import Path
from typing import TypedDict, cast

SESSION_PATH = Path.home() / ".masker" / "session.json"
SESSION_DIR = SESSION_PATH.parent


class SessionContent(TypedDict):
    masks: dict[str, str]


def create_session() -> None:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    session_content = SessionContent({"masks": {}})
    _ = SESSION_PATH.write_text(json.dumps(session_content))


def load_session() -> SessionContent:
    if not SESSION_PATH.exists():
        create_session()

    with open(SESSION_PATH) as f:
        return cast(SessionContent, json.load(f))


def save_session(data: SessionContent) -> None:
    with open(SESSION_PATH, "w") as f:
        json.dump(data, f, indent=2)


def clear_session() -> None:
    if SESSION_PATH.exists():
        SESSION_PATH.unlink()
