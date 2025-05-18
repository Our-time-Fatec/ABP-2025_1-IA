from fastapi import APIRouter, HTTPException
from app.schemas.schemas import NDVIInput, MLProcessRequest
from app.controllers.testing.nvdi import run_ndvi_pipeline
from app.services.process.pipeline import processar_imagem_completa
from app.services.process_image import process_upload_image

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
        path = await process_upload_image(data)
        return {
            "resultados_pipeline": path["resultados_pipeline"],
            "resposta_envio": path["resposta_envio"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 