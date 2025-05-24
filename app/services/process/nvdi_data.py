import numpy as np
import rasterio

def calcular_estatisticas_ndvi(ndvi_path):
    with rasterio.open(ndvi_path) as src:
        ndvi = src.read(1)
        ndvi = ndvi[np.isfinite(ndvi)]  # Remove NaNs

        # Define os intervalos (bins) do histograma
        bins = [-1.0, -0.5, 0.0, 0.2, 0.4, 0.6, 1.0]
        hist, bin_edges = np.histogram(ndvi, bins=bins)

        histogram = []
        for i in range(len(hist)):
            histogram.append({
                "range": [round(bin_edges[i], 2), round(bin_edges[i + 1], 2)],
                "count": int(hist[i])
            })

        return {
            "min": float(np.min(ndvi)),
            "max": float(np.max(ndvi)),
            "mean": float(np.mean(ndvi)),
            "std": float(np.std(ndvi)),
            "pct_acima_0_5": float(np.mean(ndvi > 0.5)) * 100,
            "histogram": histogram
        }


def calcular_area_por_classe(tif_path):
    with rasterio.open(tif_path) as src:
        mask = src.read(1)
        transform = src.transform
        res_x, res_y = transform[0], -transform[4]
        pixel_area_m2 = res_x * res_y

        classes, counts = np.unique(mask, return_counts=True)
        area_por_classe = {}
        total_pixels = 0
        burned_pixels = 0

        for cls, cnt in zip(classes, counts):
            area_m2 = cnt * pixel_area_m2
            area_ha = area_m2 / 10_000
            area_km2 = area_m2 / 1_000_000

            area_por_classe[int(cls)] = {
                "pixels": int(cnt),
                "area_m2": area_m2,
                "area_ha": area_ha,
                "area_km2": area_km2
            }

            total_pixels += cnt
            if int(cls) == 1:
                burned_pixels = cnt

        total_area_m2 = total_pixels * pixel_area_m2
        burned_area_m2 = burned_pixels * pixel_area_m2
        total_area_km2 = total_area_m2 / 1_000_000
        burned_area_km2 = burned_area_m2 / 1_000_000
        burned_percent = (burned_area_km2 / total_area_km2) * 100 if total_area_km2 else 0.0

        summary = {
            "total_area_km2": round(total_area_km2, 2),
            "burned_area_km2": round(burned_area_km2, 2),
            "burned_percent": round(burned_percent, 2)
        }

        return {
            "total_area_m2": total_area_m2,
            "total_area_ha": total_area_m2 / 10_000,
            "por_classe": area_por_classe,
            "summary": summary
        }
