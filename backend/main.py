import uuid
from datetime import datetime
from typing import Dict, Any
from threading import Lock

from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Application imports (assumes backend/ is the working directory or PYTHONPATH)
from backend.services.scan_service import run_iam_scan
from backend.services.explain_service import explain_scan_results
from backend.schemas.explain_response import ExplainResponse
from backend.utils.logger import get_logger
from backend.utils.constants import (
    APP_NAME,
    APP_VERSION,
    JOB_STATUS_IN_PROGRESS,
    JOB_STATUS_COMPLETED,
    JOB_STATUS_FAILED,
)
# --------------------------------------------------
# Logging
# --------------------------------------------------
logger = get_logger(APP_NAME)

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI(
    title="AI-Powered Cloud Security Copilot",
    description="Enterprise-grade AWS IAM security analysis using AI + RAG",
    version=APP_VERSION,
)

# --------------------------------------------------
# Middleware
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# In-Memory Job Store (Demo / Portfolio)
# --------------------------------------------------
jobs_db: Dict[str, Dict[str, Any]] = {}
jobs_lock = Lock()

# --------------------------------------------------
# Schemas
# --------------------------------------------------
class ScanJobStatus(BaseModel):
    job_id: str
    status: str
    message: str
    created_at: datetime


class ExplainRequest(BaseModel):
    scan_id: str = Field(..., description="Completed scan job ID")


# --------------------------------------------------
# Background Worker
# --------------------------------------------------
def run_scan_task(job_id: str) -> None:
    try:
        logger.info(f"[SCAN STARTED] job_id={job_id}")

        results = run_iam_scan()

        with jobs_lock:
            jobs_db[job_id].update(
                {
                    "status": JOB_STATUS_COMPLETED,
                    "data": results,
                    "finished_at": datetime.utcnow(),
                }
            )

        logger.info(f"[SCAN COMPLETED] job_id={job_id}")

    except Exception as exc:
        logger.exception(f"[SCAN FAILED] job_id={job_id}")
        with jobs_lock:
            jobs_db[job_id]["status"] = JOB_STATUS_FAILED
            jobs_db[job_id]["error"] = str(exc)


# --------------------------------------------------
# Endpoints
# --------------------------------------------------
@app.get("/health", tags=["system"])
def health_check():
    return {
        "status": "ok",
        "service": APP_NAME,
        "time": datetime.utcnow().isoformat(),
    }


@app.post(
    "/scan",
    response_model=ScanJobStatus,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["security"],
)
def start_scan(background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())

    with jobs_lock:
        jobs_db[job_id] = {
            "status": JOB_STATUS_IN_PROGRESS,
            "data": None,
            "created_at": datetime.utcnow(),
        }

    background_tasks.add_task(run_scan_task, job_id)

    return {
        "job_id": job_id,
        "status": JOB_STATUS_IN_PROGRESS,
        "message": "IAM scan initiated",
        "created_at": jobs_db[job_id]["created_at"],
    }


@app.get("/scan/{job_id}", tags=["security"])
def get_scan_status(job_id: str):
    with jobs_lock:
        job = jobs_db.get(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan job not found",
        )

    return job


@app.post(
    "/explain",
    response_model=ExplainResponse,
    tags=["ai"],
)
def explain_scan(request: ExplainRequest):
    with jobs_lock:
        job = jobs_db.get(request.scan_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan job not found",
        )

    if job["status"] != JOB_STATUS_COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scan not completed yet",
        )

    logger.info(f"[AI EXPLAIN] scan_id={request.scan_id}")

    return explain_scan_results(job["data"])
