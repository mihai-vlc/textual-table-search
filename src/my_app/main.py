from pathlib import Path
import sqlite3
from pprint import pprint
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import DataTable, Input, Header, Button
from textual.containers import Horizontal, Vertical

db_path = Path("data/data.db").resolve()


class CustomApp(App):
    CSS = """
        .search_input {
            width: 80%;
        }
        .search_btn {
            width: 20%;
        }

        Screen {
        }

        .data_table {
            max-height: 88vh;
        }
        .search_box {
            height: auto;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(classes="search_box"):
            yield Input(placeholder="Search", classes="search_input")
            yield Button(label="Search", variant="primary", classes="search_btn")

        yield DataTable(classes="data_table")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "none"
        table.zebra_stripes = True
        table.add_columns("id", "first_name", "last_name",
                          "email", "gender", "ip_address")
        rows = get_users()
        table.add_rows(rows)
        search_input = self.query_one(".search_input")
        self.set_focus(search_input)

    def on_input_submitted(self,  message: Input.Changed) -> None:
        self.update_table(message.value)

    def on_button_pressed(self) -> None:
        search_input = self.query_one(".search_input")
        self.update_table(search_input.value)
        pass

    def update_table(self, query: str = ""):
        rows = get_users(query)
        table = self.query_one(DataTable)
        table.clear()
        table.add_rows(rows)


def get_users(query=""):
    con = sqlite3.connect(db_path)
    q = "SELECT id, first_name, last_name, email, gender, ip_address FROM users WHERE first_name LIKE ? OR last_name LIKE ?"
    result = con.execute(q, [f"%{query}%", f"%{query}%"])

    return iter(result)


def run() -> int:

    app = CustomApp()
    app.run()

    return 0


if __name__ == "__main__":
    exit(run())
