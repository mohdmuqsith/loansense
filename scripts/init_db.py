from pathlib import Path
import os

import psycopg2


ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "backend" / "db"

SQL_FILES = [
    "schema.sql",
    "functions.sql",
    "procedures.sql",
    "triggers.sql",
    "views.sql",
    "indexes.sql",
    "seed.sql",
]


def main() -> None:
    database_url = os.environ["DATABASE_URL"]

    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            for filename in SQL_FILES:
                path = DB_DIR / filename
                print(f"Running {path.relative_to(ROOT)}")
                cur.execute(path.read_text(encoding="utf-8"))
        conn.commit()

    print("Database initialized.")


if __name__ == "__main__":
    main()
