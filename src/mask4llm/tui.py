from typing import override

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, TextArea

from mask4llm.masking import mask, unmask
from mask4llm.session import load_session, save_session
from mask4llm.util import display_dict_in_json_format, pipe_str
from mask4llm.widgets.copy_on_enter_log import CopyOnEnterLog


class MaskerApp(App[None]):
    CSS_PATH = "styles.tcss"  # pyright: ignore[reportUnannotatedClassAttribute]

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Vertical(
                Container(
                    Label("Input"),
                    TextArea(
                        id="id-input-text",
                        show_line_numbers=True,
                        text=f"{'\n' * 4}",
                        line_number_start=1,
                    ),
                    id="id-input-container",
                ),
                Container(
                    Label("Pattern(s)"),
                    Input(
                        id="id-pattern-input",
                        placeholder="comma-separated pattern(s)",
                    ),
                    id="id-pattern-input-container",
                ),
                Container(
                    Button("mask", variant="success", id="id-mask-btn"),
                    Button("unmask", variant="warning", id="id-unmask-btn"),
                    id="id-button-container",
                ),
                Container(
                    Label(
                        "Output (Enter or Press y to copy)",
                        id="id-output-log-label",
                    ),
                    CopyOnEnterLog(id="id-output-log", highlight=True),
                    id="id-output-log-container",
                ),
            )
            yield Container(
                Label(
                    "Mask Map (Enter or Press y to copy)",
                    id="id-mask-map-label",
                ),
                CopyOnEnterLog(id="id-mask-map-log", highlight=True),
                id="id-mask-map-log-container",
            )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        input_text = self.query_one("#id-input-text", TextArea).text.strip()

        input_patterns_str = self.query_one("#id-pattern-input", Input).value
        input_patterns = pipe_str(input_patterns_str)

        output_log = self.query_one("#id-output-log", CopyOnEnterLog)
        mask_map_log = self.query_one("#id-mask-map-log", CopyOnEnterLog)

        session = load_session()
        mask_map = session["masks"]
        if event.button.id == "id-mask-btn":
            if not input_text and len(input_patterns) == 1:
                self.notify(
                    "Input | Pattern(s) [b]cannot be empty[/b].",
                    title="Error",
                    timeout=4,
                    severity="error",
                )
                return

            masked_text, new_map = mask(input_text, input_patterns)
            mask_map.update(new_map)
            session["masks"] = mask_map
            save_session(session)
            _ = output_log.clear().write(masked_text)

        elif event.button.id == "id-unmask-btn":
            if not input_text:
                self.notify(
                    "Input [b]cannot be empty[/b].",
                    title="Error",
                    timeout=4,
                    severity="error",
                )
                return
            unmasked_text = unmask(input_text, mask_map)
            _ = output_log.clear().write(unmasked_text)

        save_session(session)
        _ = mask_map_log.clear()
        display_dict_in_json_format(mask_map_log, mask_map)

    async def on_copy_on_enter_log_copied(
        self, message: CopyOnEnterLog.Copied
    ):
        copied_length = len(message.content)

        feedback = Text(
            f"\n✅ Copied {copied_length} characters to clipboard",
            style="green",
        )
        self.notify(str(feedback), timeout=2, title="Copied!")


def run_tui():
    masker_app = MaskerApp()
    masker_app.run()
