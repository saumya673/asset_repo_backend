import uvicorn
from fastapi import Depends, FastAPI, Query, Response

from models import Project
from services.db.base import DBClient
from services.db.sqlite import get_sqlite_db

app = FastAPI()


@app.get("/projects")
def projects(
    response: Response,
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: DBClient = Depends(get_sqlite_db),
) -> list[Project]:
    response.headers["page-num"] = str(page_num)
    response.headers["page-size"] = str(page_size)
    return db.get_projects(page_num=page_num, page_size=page_size)


def main():
    uvicorn.run(app="main:app", reload=True)


if __name__ == "__main__":
    main()
