from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
from fastapi.responses import FileResponse
from workflows.summarization_workflow import summarization_workflow
from models.summarymodel import SummaryResponse
from utils.file_utils import save_uploaded_file, save_file, delete_file, list_summaries
from core.logger_config import logger
from core.llm_cost import LLMCost
from core.config import settings
from utils.auth_utils import get_current_user

import os

router = APIRouter(tags=["Summarization"])
process_name = "Summarization"

@router.get("/ping")
async def ping():
    return {"status": "pong"}

@router.post("/extract", response_model=SummaryResponse)
async def extract_scientific_summary(
    file: UploadFile = File(...),
    folder: str = Query("articles"),
    current_user: str = Depends(get_current_user)
):
    try:
        logger.info(f"Received file: {file.filename}")
        folder_path = os.path.join(settings.USER_WORKDIR, folder)
        os.makedirs(folder_path, exist_ok=True)

        # ✅ Save PDF into the correct folder
        pdf_path = await save_uploaded_file(file, folder_path)
        logger.info(f"Saved PDF to: {pdf_path}")

        # 🧠 Run summarization workflow
        summary_result = summarization_workflow.kickoff(inputs={"pdf_path": pdf_path})

        # 💰 Track token usage
        token_count = (
            summarization_workflow.usage_metrics.prompt_tokens +
            summarization_workflow.usage_metrics.completion_tokens
        )
        LLMCost.update_cost(process_name, token_count)

        return summary_result.to_dict()

    except Exception as e:
        logger.error("Error during summarization", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/load/{filename}", response_model=dict)
async def load_summary(
    filename: str,
    folder: str = Query("articles"),
    current_user: str = Depends(get_current_user)
):
    folder_path = os.path.join(settings.USER_WORKDIR, folder)
    filepath = os.path.join(folder_path, filename if filename.endswith(".txt") else f"{os.path.splitext(filename)[0]}.txt")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Summary file not found")

    with open(filepath, "r", encoding="utf-8") as f:
        return {"message": "Summary loaded successfully", "content": f.read(), "filename": filename}

@router.post("/save", response_model=dict)
async def save_summary(
    data: SummaryResponse,
    folder: str = Query("articles"),
    current_user: str = Depends(get_current_user)
):
    folder_path = os.path.join(settings.USER_WORKDIR, folder)
    os.makedirs(folder_path, exist_ok=True)
    filename = f"{os.path.splitext(data.filename)[0]}.txt"
    path = os.path.join(folder_path, filename)
    save_file(path, data.summary)
    return {"message": "Summary saved successfully", "filename": filename}

@router.get("/list", response_model=dict)
async def get_summaries(
    folder: str = Query("articles"),
    current_user: str = Depends(get_current_user)
):
    folder_path = os.path.join(settings.USER_WORKDIR, folder)
    return {"summaries": list_summaries(folder_path)}

@router.delete("/{filename}", response_model=dict)
async def delete_summary(
    filename: str,
    folder: str = Query("articles"),
    current_user: str = Depends(get_current_user)
):
    folder_path = os.path.join(settings.USER_WORKDIR, folder)
    path = os.path.join(folder_path, filename)
    delete_file(path)
    return {"message": "Summary deleted successfully"}

@router.get("/pdf/{filename}")
async def get_pdf(
    filename: str,
    folder: str = Query("articles"),
    current_user: str = Depends(get_current_user)
):
    folder_path = os.path.join(settings.USER_WORKDIR, folder)
    path = os.path.join(folder_path, filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="application/pdf")
    raise HTTPException(status_code=404, detail="PDF not found")

@router.get("/files", response_model=dict)
async def list_files(
    folder: str = Query(...),
    current_user: str = Depends(get_current_user)
):
    folder_path = os.path.join(settings.USER_WORKDIR, folder)
    if not os.path.exists(folder_path):
        raise HTTPException(status_code=404, detail="Folder not found")
    filenames = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    return {"files": filenames}

