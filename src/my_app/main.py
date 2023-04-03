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
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns('id', 'first_name', 'last_name')
        rows = get_users()
        table.add_rows(rows)


def get_users():
    con = sqlite3.connect(db_path)
    q = "SELECT id, first_name, last_name FROM users WHERE gender IN (?, ?) LIMIT 50"
    result = con.execute(q, ["Male", "Female"])

    return iter(result)


def run() -> int:

    app = CustomApp()
    app.run()

    return 0


if __name__ == "__main__":
    exit(run())
