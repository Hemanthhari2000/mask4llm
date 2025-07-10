from textual.app import App
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, TextArea


class MaskerApp(App):
    CSS_PATH = "styles.tcss"

    def compose(self):
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
                ),
            )
            yield Container(
                Label(
                    "Mask Map (Enter or Press y to copy)",
                    id="id-mask-map-label",
                ),
            )
        yield Footer()

    def on_button_pressed(self, _: Button.Pressed): ...


def run_tui():
    MaskerApp().run()
