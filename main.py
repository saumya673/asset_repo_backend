import uvicorn
from fastapi import Depends, FastAPI, Query, Response, UploadFile, File, HTTPException
import tempfile
from openai import AzureOpenAI
from services.ppt import extract_text_from_pptx
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


@app.post("/create-project")
async def chat(file: UploadFile = File(...)):
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
    
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2025-03-01-preview",
    )

    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes PowerPoint presentations."
                },
                {
                    "role": "user",
                    "content": f"""
Analyze this PowerPoint content and summarize it clearly.

PowerPoint content:

{ppt_text}
"""
                }
            ]
        )

        return {
            "filename": file.filename,
            "extracted_text": ppt_text,
            "answer": response.choices[0].message.content
        }
    except Exception as e:
        raise e

def main():
    uvicorn.run(app="main:app", reload=True)


if __name__ == "__main__":
    main()
