import pyperclip
from textual.message import Message
from textual.widgets import Log


class CopyOnEnterLog(Log):
    class Copied(Message):
        content: str

        def __init__(self, sender: "CopyOnEnterLog", content: str) -> None:
            self.content = content
            super().__init__()

    def key_enter(self) -> None:
        self.copy_to_clipboard()

    def key_y(self) -> None:
        self.copy_to_clipboard()

    def copy_to_clipboard(self) -> None:
        content = "\n".join(self.lines)
        pyperclip.copy(content)
        _ = self.post_message(self.Copied(self, content))
