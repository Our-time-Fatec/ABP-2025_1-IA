import os
import rasterio
from app.schemas.schemas import MLProcessRequest
from app.utils.download_util import baixar_arquivo
from app.services.process.nvdi import compute_ndvi
from app.services.process.visualization import save_ndvi_preview
from app.services.process.segmentation import run_model

async def processar_imagem_completa(data: MLProcessRequest):
    
    print(f"🟡 Iniciando processamento de {data.id}")
    print(f"👉 BAND15 URL: {data.band15_url}")
    print(f"👉 BAND16 URL: {data.band16_url}")

    red_path = f"app/data/raw/{data.id}_BAND15.tif"
    nir_path = f"app/data/raw/{data.id}_BAND16.tif"
    ndvi_tif = f"app/data/processed/{data.id}_ndvi.tif"
    ndvi_preview = f"app/data/processed/{data.id}_ndvi_preview.png"

    baixar_arquivo(data.band15_url, red_path)
    baixar_arquivo(data.band16_url, nir_path)

    compute_ndvi(red_path, nir_path, ndvi_tif, lambda ndvi: save_ndvi_preview(ndvi, ndvi_preview))

    tif_final, png_final = run_model(ndvi_tif, data.id)

    with rasterio.open(tif_final) as src:
        bounds = src.bounds
        real_bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        
        

    return {
        "preview_png": f"/output/{data.id}_rgb.png",
        "preview_tif": f"/output/{data.id}_classes.tif",
        "bbox": data.bbox,
        "bbox_real": real_bbox
    }
