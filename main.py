import uvicorn
from fastapi import Depends, FastAPI, Query, Response
from openai import AzureOpenAI
from models import Project
from services.db.base import DBClient
from services.db.sqlite import get_sqlite_db
from dotenv import load_dotenv
import os

load_dotenv()

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

@app.post("/chat")
def chat(msg: str):
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2025-03-01-preview"
    )

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "user", "content": msg}
        ]
    )

    return response










def main():
    uvicorn.run(app="main:app", reload=True)


if __name__ == "__main__":
    main()
