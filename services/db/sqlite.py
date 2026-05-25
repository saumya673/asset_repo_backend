import sqlite3
import json
from models import Project
from services.db.base import DBClient


class SqliteDB(DBClient):

    def __init__(self):
        self.con = sqlite3.connect("asset_repo.db")
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS projects(id UUID PRIMARY KEY, info JSONB, full_ppt TEXT)")

    def get_projects(self, page_num: int, page_size: int) -> list[Project]:
        if page_num < 1:
            raise ValueError("page_num must be >= 1")
        if page_size < 1:
            raise ValueError("page_size must be >= 1")

        offset = (page_num - 1) * page_size
        cursor = self.cur
        cursor.execute(
            "SELECT id, info FROM projects ORDER BY id LIMIT ? OFFSET ?",
            (page_size, offset),
        )
        rows = cursor.fetchall()

        projects: list[Project] = []
        for row in rows:
            payload = row["info"]
            project_data = json.loads(payload) if isinstance(payload, str) else payload
            projects.append(Project.model_validate(project_data))

        return projects
    

def get_sqlite_db():
    return SqliteDB()
