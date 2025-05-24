from fastapi import APIRouter, HTTPException
from app.schemas.schemas import NDVIInput, MLProcessRequest
from app.controllers.testing.nvdi import run_ndvi_pipeline
from app.services.process.pipeline import processar_imagem_completa
from app.services.testing.process_image import process_upload_image_mock
from app.services.process_image import process_upload_image
import uuid
from fastapi.responses import JSONResponse
from app.schemas.schemas import InitProcessResponse
from app.services.job_manager import job_manager
import asyncio 

router = APIRouter(prefix="/ndvi", tags=["NDVI"])

@router.post("")
def ndvi(data: NDVIInput):
    try:
        path = run_ndvi_pipeline(data.red_url, data.nir_url)
        return {"mask_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v1")
async def ndvi2(data: MLProcessRequest):
    try:
        path = await processar_imagem_completa(data)
        return {"mask_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v2")
async def ndvi_upload(data: MLProcessRequest):
    try:
        path = await process_upload_image(data, "v2")
        return {
            "resultados_pipeline": path["resultados_pipeline"],
            "resposta_envio": path["resposta_envio"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v3", response_model=InitProcessResponse)
async def ndvi_upload_job(data: MLProcessRequest):
    job_id = str(uuid.uuid4())
    job_manager.create_job(job_id)

    async def background_task():
        try:
            result = await process_upload_image(data, job_id)
            job_manager.update_job(job_id, status="completed", result=result)
        except Exception as e:
            job_manager.update_job(job_id, status="failed", result={"error": str(e)})

    asyncio.create_task(background_task())

    return InitProcessResponse(
        jobId=job_id,
        status="processing",
        message="Processamento iniciado com sucesso."
    )


@router.post("/v3/mock")
async def nvdi_test(data: MLProcessRequest):
    
    job_id = str(uuid.uuid4())
    job_manager.create_job(job_id)
    
    try:
        path = await process_upload_image_mock(data, job_id)
        return {
            "resultados_pipeline": path["resultados_pipeline"],
            "resposta_envio": path["resposta_envio"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))