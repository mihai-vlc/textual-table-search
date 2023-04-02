from pathlib import Path
import sqlite3

base_path = Path(__file__).parent
db_path = base_path.joinpath("../data/data.db").resolve()


def execute_file(cursor: sqlite3.Cursor, file: Path):
    try:
        print(f"{file.name}: starting migration")
        cursor.executescript(f"""
            BEGIN;
            {file.read_text()}
            COMMIT;
        """)
        cursor.execute("INSERT INTO migrations (name) VALUES (?)", [file.name])
        print(f"{file.name}: completed migration")
    except Exception as err:
        print(f"{file.name}: failed migration: {err=}, {type(err)=}")


def run() -> int:
    connection = sqlite3.connect(db_path.absolute())
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            name VARCHAR(255) NOT NULL,
            executed_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    result = cursor.execute("SELECT name from migrations")
    processed_files = [row[0] for row in result]

    all_files = sorted(base_path.glob("*.sql"))

    for file in all_files:
        if file.name not in processed_files:
            execute_file(cursor, file)
            connection.commit()
        else:
            print(f"{file.name}: skipped")

    return 0


if __name__ == "__main__":
    exit(run())
