from fastapi import FastAPI, HTTPException
from src.schemas import ImageInput, NDVIInput, RGBInput, MLProcessRequest
from src.controllers.test.inference import run_inference_from_cog_url as run_inference
from src.controllers.test.nvdi import run_ndvi_pipeline
from src.controllers.test.rgb_segment import run_rgb_segmentation
from src.controllers.services.nvdi_pipeline import processar_imagem_completa

app = FastAPI()

@app.post("/segment")
def segment(data: ImageInput):
    try:
        path = run_inference(data.url)
        return {"mask_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ndvi")
def ndvi(data: NDVIInput):
    try:
        path = run_ndvi_pipeline(data.red_url, data.nir_url)
        return {"mask_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/ndvi2")
async def ndvi2(data: MLProcessRequest):
    try:
        path = await processar_imagem_completa(data)
        return {"mask_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/segment-rgb")
def segment_rgb(data: RGBInput):
    try:
        path = run_rgb_segmentation(data.band13_url, data.band15_url, data.band16_url)
        return {"mask_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
