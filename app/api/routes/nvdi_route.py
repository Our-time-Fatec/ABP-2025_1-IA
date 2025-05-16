from fastapi import APIRouter, HTTPException
from app.schemas.schemas import NDVIInput, MLProcessRequest
from app.controllers.testing.nvdi import run_ndvi_pipeline
from app.services.nvdi_pipeline import processar_imagem_completa

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
