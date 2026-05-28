from typing import Annotated

import uvicorn
from fastapi import Body, Depends, FastAPI, Query, Response, UploadFile, File, HTTPException, Form

from services.llm import analyze_ppt
from services.ppt import extract_text_from_pptx
from models import Project
from services.db.base import DBClient
from services.db.sqlite import get_sqlite_db
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/assets")
def projects(
    response: Response,
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db: DBClient = Depends(get_sqlite_db),
) -> list[Project]:
    response.headers["page-num"] = str(page_num)
    response.headers["page-size"] = str(page_size)
    return db.get_projects(page_num=page_num, page_size=page_size)


@app.post("/save-asset")
async def chat(file: UploadFile = File(...), db: DBClient = Depends(get_sqlite_db)):
    if not file.filename.endswith(".pptx"):
        raise HTTPException(
            status_code=400,
            detail="Only .pptx files are supported"
        )

    contents = await file.read()

    ppt_text = extract_text_from_pptx(contents)

    if not ppt_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the PPT file"
        )

    existing_project = db.get_project_by_ppt_text(ppt_text)
    if existing_project is not None:
        return {
            "answer": existing_project
        }

    try:
        result = await analyze_ppt(ppt_text=ppt_text)
        db.save_project(id=result.id,project=result,ppt_text=ppt_text) #id, project, project ppt in text
        return {
            "answer": result
        }
    except Exception as e:
        raise e


@app.put("/update-asset", response_model=Project)
async def update_asset(
    asset_input: Annotated[Project, Body()],
    db: DBClient = Depends(get_sqlite_db),
):
    project_id = asset_input.id

    existing_project = db.get_project_by_id(project_id)
    if existing_project is None:
        raise HTTPException(
            status_code=404,
            detail=f"Project {project_id} not found",
        )

    return db.update_project(project_id, asset_input)


def main():
    uvicorn.run(app="main:app", reload=True)


if __name__ == "__main__":
    main()
