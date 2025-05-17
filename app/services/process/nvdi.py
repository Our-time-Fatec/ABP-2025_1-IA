import numpy as np
import rasterio
from rasterio.coords import BoundingBox
from rasterio.windows import from_bounds

def compute_ndvi(red_path, nir_path, output_path, preview_callback=None):
    print(f"📥 Abrindo RED: {red_path} e NIR: {nir_path}")
      
    with rasterio.open(red_path) as red, rasterio.open(nir_path) as nir:
        intersection = get_common_bounds(red.bounds, nir.bounds)

        red_window = from_bounds(*intersection, transform=red.transform)
        nir_window = from_bounds(*intersection, transform=nir.transform)

        red_data = red.read(1, window=red_window).astype("float32")
        nir_data = nir.read(1, window=nir_window).astype("float32")

        if red_data.shape != nir_data.shape:
            raise ValueError("As janelas de RED e NIR resultam em tamanhos diferentes.")
        
        print(f"📏 Shape comum: {red_data.shape}")

        ndvi = calculate_ndvi(nir_data, red_data)

        profile = red.profile
        profile.update(
            dtype="float32",
            count=1,
            height=ndvi.shape[0],
            width=ndvi.shape[1],
            transform=rasterio.windows.transform(red_window, red.transform) # type: ignore
        )

        print(f"💾 Salvando NDVI em: {output_path}")
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(ndvi, 1)

        if preview_callback:
            preview_callback(ndvi)

def get_common_bounds(bounds1, bounds2):
    return BoundingBox(
        left=max(bounds1.left, bounds2.left),
        bottom=max(bounds1.bottom, bounds2.bottom),
        right=min(bounds1.right, bounds2.right),
        top=min(bounds1.top, bounds2.top)
    )

def calculate_ndvi(nir, red):
    print("🧮 Calculando NDVI...")
    ndvi = (nir - red) / (nir + red + 1e-10)
    return np.clip(ndvi, -1, 1)
