from mask4llm.session import create_session
from mask4llm.tui import run_tui


def main() -> None:
    create_session()
    run_tui()
