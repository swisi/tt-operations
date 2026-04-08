#!/usr/bin/env python3
import argparse
import sqlite3
import sys

import psycopg


TABLES = [
    "users",
    "services",
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
    if column == "is_active" and value is not None:
        return bool(value)
    return value


def copy_table(pg_conn, table_name, rows):
    with pg_conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
        if not rows:
            return
        target_columns = get_target_columns(pg_conn, table_name)
        columns = [column for column in rows[0].keys() if column in target_columns]
        placeholders = ", ".join(["%s"] * len(columns))
        column_sql = ", ".join(columns)
        values = [
            [normalize_value(column, row[column]) for column in columns]
            for row in rows
        ]
        cur.executemany(
            f"INSERT INTO {table_name} ({column_sql}) VALUES ({placeholders})",
            values,
        )


def main():
    parser = argparse.ArgumentParser(description="Migrate tt-auth data from SQLite to PostgreSQL.")
    parser.add_argument("--sqlite-path", required=True, help="Path to auth.db")
    parser.add_argument("--postgres-dsn", required=True, help="PostgreSQL DSN")
    args = parser.parse_args()

    try:
        sqlite_conn = sqlite3.connect(args.sqlite_path)
    except sqlite3.Error as exc:
        print(f"Failed to open SQLite database: {exc}", file=sys.stderr)
        return 1

    try:
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
