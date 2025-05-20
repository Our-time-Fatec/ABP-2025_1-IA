from fastapi import APIRouter, HTTPException
from app.services.job_manager import job_manager

router = APIRouter(prefix="/check", tags=["Status"])

@router.get("/status/{job_id}")
def get_job_status(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID não encontrado.")
    return {"jobId": job_id, "status": job["status"], "result": job["result"]}

@router.get("")
def check():
    return {"message": "IA em funcionamento!"}