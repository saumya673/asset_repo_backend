from contextlib import asynccontextmanager
from fastapi import FastAPI
import sqlite3
from pathlib import Path
import csv


DB_PATH = Path("asset_repo.db")
TRACKER_CSV_PATH = Path("assets/unstoppable_stories_tracker_sample.csv")


def extract_file_id(serial: str) -> str:
    if "#" not in serial:
        return serial.strip()

    return serial.split("#", 1)[1].strip()


def initialize_tracker_metadata():
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS asset_file_metadata (
                file_id TEXT PRIMARY KEY,
                isu TEXT NOT NULL DEFAULT '',
                subisu TEXT NOT NULL DEFAULT '',
                account TEXT NOT NULL DEFAULT ''
            )
            """
        )

        if not TRACKER_CSV_PATH.exists():
            return

        with TRACKER_CSV_PATH.open(newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                file_id = extract_file_id(row.get("S#", ""))
                if not file_id:
                    continue

                con.execute(
                    """
                    INSERT INTO asset_file_metadata (file_id, isu, subisu, account)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(file_id) DO UPDATE SET
                        isu = excluded.isu,
                        subisu = excluded.subisu,
                        account = excluded.account
                    """,
                    (
                        file_id,
                        "",
                        row.get("Unit/Sub Unit", "").strip(),
                        row.get("Group/Account", "").strip(),
                    ),
                )

        con.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_tracker_metadata()
    yield