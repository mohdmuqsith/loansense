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

DEMO_PASSWORD_HASH = "$2b$12$fC56Sj/FxMtQJyXoJ8veIuQuA2CcFhy6kjDIZHmv7zBL/eI0vQCeq"


def database_is_initialized(cur) -> bool:
    cur.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name IN ('bank_managers', 'loan_applications')
        """
    )
    return cur.fetchone()[0] > 0


def sync_demo_passwords(cur) -> None:
    cur.execute(
        """
        UPDATE bank_managers
        SET password_hash = %s
        WHERE username IN ('admin', 'manager1', 'manager2')
        """,
        (DEMO_PASSWORD_HASH,),
    )


def main() -> None:
    database_url = os.environ["DATABASE_URL"]
    reset_database = os.getenv("RESET_DATABASE", "").lower() in {"1", "true", "yes"}

    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            if database_is_initialized(cur) and not reset_database:
                sync_demo_passwords(cur)
                conn.commit()
                print("Database already initialized. Skipping schema load.")
                return

            for filename in SQL_FILES:
                path = DB_DIR / filename
                print(f"Running {path.relative_to(ROOT)}")
                cur.execute(path.read_text(encoding="utf-8"))
            sync_demo_passwords(cur)
        conn.commit()

    print("Database initialized.")


if __name__ == "__main__":
    main()
