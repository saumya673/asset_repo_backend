import sqlite3
import json
from uuid import UUID
from models import Project
from services.db.base import DBClient


class SqliteDB(DBClient):
    def __init__(self):
        self.con = sqlite3.connect(
            "asset_repo.db",
            check_same_thread=False
        )
        self.con.row_factory = sqlite3.Row
        self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                info JSONB NOT NULL,
                full_ppt TEXT NOT NULL
            )
            """
        )
        self.con.commit()

    def close(self):
        self.con.close()

    def get_projects(self, page_num: int, page_size: int) -> list[Project]:
        offset = (page_num - 1) * page_size

        cursor = self.con.execute(
            """
            SELECT id, info
            FROM projects
            ORDER BY id
            LIMIT ? OFFSET ?
            """,
            (page_size, offset),
        )

        rows = cursor.fetchall()

        projects: list[Project] = []
        for row in rows:
            payload = row["info"]
            project_data = json.loads(payload) if isinstance(payload, str) else payload
            projects.append(Project.model_validate(project_data))
        
        return projects

    def get_project_by_ppt_text(self, ppt_text: str) -> Project | None:
        cursor = self.con.execute(
            """
            SELECT info
            FROM projects
            WHERE full_ppt = ?
            LIMIT 1
            """,
            (ppt_text,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        payload = row["info"]
        project_data = json.loads(payload) if isinstance(payload, str) else payload
        return Project.model_validate(project_data)

    def get_project_by_id(self, id: UUID) -> Project | None:
        cursor = self.con.execute(
            """
            SELECT info
            FROM projects
            WHERE id = ?
            LIMIT 1
            """,
            (str(id),),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        payload = row["info"]
        project_data = json.loads(payload) if isinstance(payload, str) else payload
        return Project.model_validate(project_data)

    def save_project(self, id: UUID, project: Project, ppt_text: str) -> Project:
        stored_project = project.model_copy(update={"id": id})
        payload = json.dumps(stored_project.model_dump(mode="json"))

        self.con.execute(
            """
            INSERT INTO projects (id, info, full_ppt)
            VALUES (?, ?, ?)
            """,
            (str(id), payload, ppt_text),
        )
        self.con.commit()

        return stored_project

    def update_project(self, id: UUID, project: Project) -> Project:
        stored_project = project.model_copy(update={"id": id})
        payload = json.dumps(stored_project.model_dump(mode="json"))

        cursor = self.con.execute(
            """
            UPDATE projects
            SET info = ?
            WHERE id = ?
            """,
            (payload, str(id)),
        )
        self.con.commit()

        if cursor.rowcount == 0:
            raise KeyError(f"Project {id} not found")

        return stored_project


def get_sqlite_db():
    db = SqliteDB()
    try:
        yield db
    finally:
        db.close()
