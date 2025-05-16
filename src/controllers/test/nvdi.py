import rasterio
import numpy as np
import requests
from tempfile import NamedTemporaryFile
import os
from PIL import Image

def download_tiff(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    tmp = NamedTemporaryFile(delete=False, suffix=".tif")
    tmp.write(response.content)
    tmp.close()
    return tmp.name

def calculate_ndvi_from_urls(red_url: str, nir_url: str) -> np.ndarray:
    red_path = download_tiff(red_url)
    nir_path = download_tiff(nir_url)

    with rasterio.open(red_path) as src_red, rasterio.open(nir_path) as src_nir:
        red = src_red.read(1).astype("float32")
        nir = src_nir.read(1).astype("float32")

    os.remove(red_path)
    os.remove(nir_path)

    np.seterr(divide="ignore", invalid="ignore")
    ndvi = (nir - red) / (nir + red)
    ndvi = np.nan_to_num(ndvi, nan=0.0)
    return ndvi

def classify_ndvi(ndvi: np.ndarray, threshold: float = 0.2) -> np.ndarray:
    return (ndvi >= threshold).astype("uint8")

def save_ndvi_mask(mask: np.ndarray, path: str = "masks/ndvi_mask.png") -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.fromarray(mask * 255)  # binário → imagem preta/branca
    img.save(path)
    return path

def run_ndvi_pipeline(red_url: str, nir_url: str, output_path: str = "masks/ndvi_mask.png") -> str:
    ndvi = calculate_ndvi_from_urls(red_url, nir_url)
    mask = classify_ndvi(ndvi)
    return save_ndvi_mask(mask, output_path)
