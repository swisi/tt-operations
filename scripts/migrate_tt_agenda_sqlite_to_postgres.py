#!/usr/bin/env python3
import argparse
import json
import sqlite3
import sys
from pathlib import Path

import psycopg


TABLES = [
    "user",
    "activity_type",
    "training",
    "activity",
    "training_instance",
    "activity_instance",
]

LEGACY_TABLES = [
    "training_type",
]


def fetch_rows(sqlite_conn, table_name):
    sqlite_conn.row_factory = sqlite3.Row
    rows = sqlite_conn.execute(f"SELECT * FROM {table_name} ORDER BY id").fetchall()
    return [dict(row) for row in rows]


def get_target_columns(pg_conn, table_name):
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
            """,
            (table_name,),
        )
        return [row[0] for row in cur.fetchall()]


def normalize_value(column, value):
    if column == "is_hidden" and value is not None:
        return bool(value)
    return value


def copy_table(pg_conn, table_name, rows):
    with pg_conn.cursor() as cur:
        cur.execute(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE')
        if not rows:
            return
        target_columns = get_target_columns(pg_conn, table_name)
        columns = [column for column in rows[0].keys() if column in target_columns]
        placeholders = ", ".join(["%s"] * len(columns))
        column_sql = ", ".join(f'"{column}"' for column in columns)
        values = [
            [normalize_value(column, row[column]) for column in columns]
            for row in rows
        ]
        cur.executemany(
            f'INSERT INTO "{table_name}" ({column_sql}) VALUES ({placeholders})',
            values,
        )


def archive_legacy_tables(sqlite_conn, archive_dir):
    archive_dir.mkdir(parents=True, exist_ok=True)
    for table_name in LEGACY_TABLES:
        rows = fetch_rows(sqlite_conn, table_name)
        if not rows:
            continue
        output_path = archive_dir / f"{table_name}.json"
        output_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Archived legacy table {table_name} to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Migrate tt-agenda data from SQLite to PostgreSQL.")
    parser.add_argument("--sqlite-path", required=True, help="Path to trainings.db")
    parser.add_argument("--postgres-dsn", required=True, help="PostgreSQL DSN")
    parser.add_argument(
        "--archive-dir",
        default="migration-archive",
        help="Directory for archived legacy SQLite-only tables",
    )
    args = parser.parse_args()

    try:
        sqlite_conn = sqlite3.connect(args.sqlite_path)
    except sqlite3.Error as exc:
        print(f"Failed to open SQLite database: {exc}", file=sys.stderr)
        return 1

    archive_dir = Path(args.archive_dir)

    try:
        archive_legacy_tables(sqlite_conn, archive_dir)
        with psycopg.connect(args.postgres_dsn) as pg_conn:
            for table_name in TABLES:
                rows = fetch_rows(sqlite_conn, table_name)
                copy_table(pg_conn, table_name, rows)
                print(f"Migrated {len(rows)} rows into {table_name}")
            pg_conn.commit()
    except Exception as exc:
        print(f"PostgreSQL migration failed: {exc}", file=sys.stderr)
        return 1
    finally:
        sqlite_conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
