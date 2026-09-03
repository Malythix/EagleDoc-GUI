from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import httpx
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

EAGLE_DOC_ENDPOINTS = [
    {"label": "Eagle Doc DE", "value": "https://de.eagle-doc.com"},
]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "endpoints": EAGLE_DOC_ENDPOINTS,
        "default_api_key": os.getenv("EAGLE_DOC_API_KEY", ""),
    })


@app.post("/submit/learning")
async def submit_learning(
    base_url: str = Form(...),
    api_key: str = Form(...),
    sub_business_ref: Optional[str] = Form(None),
    file: UploadFile = File(...),
    original: UploadFile = File(...),
    corrected: UploadFile = File(...),
):
    url = f"{base_url}/api/docu/learning"
    headers = {"api-key": api_key}
    if sub_business_ref and sub_business_ref.strip():
        headers["x-sub-business-ref"] = sub_business_ref.strip()

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            url,
            headers=headers,
            files={
                "file": (file.filename, await file.read(), file.content_type),
                "original": (original.filename, await original.read(), original.content_type),
                "corrected": (corrected.filename, await corrected.read(), corrected.content_type),
            },
        )

    return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/submit/instructions")
async def submit_instructions(
    base_url: str = Form(...),
    api_key: str = Form(...),
    sub_business_ref: Optional[str] = Form(None),
    instructions: str = Form(...),
    overwrite: bool = Form(False),
    corrected: UploadFile = File(...),
):
    url = f"{base_url}/api/docu/learning/instructions"
    headers = {"api-key": api_key}
    if sub_business_ref and sub_business_ref.strip():
        headers["x-sub-business-ref"] = sub_business_ref.strip()

    params = {
        "instructions": instructions,
        "overwrite": str(overwrite).lower(),
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            url,
            headers=headers,
            params=params,
            files={
                "corrected": (corrected.filename, await corrected.read(), corrected.content_type),
            },
        )

    return JSONResponse(status_code=response.status_code, content=response.json())
