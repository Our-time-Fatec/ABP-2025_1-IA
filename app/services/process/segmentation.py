import os
import numpy as np
import torch
import rasterio
from PIL import Image, ImageDraw
from app.utils.model import get_unet_model

COLORS = {
    1: (255, 0, 0, 255),
    2: (124, 94, 21, 255),
    3: (16, 149, 9, 255),
}

def run_model(ndvi_path, output_prefix, model_path="app/models/final_model_1.pth"):
    tile_size = 256
    stride = 128
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    output_tif = os.path.join(output_dir, f"{output_prefix}_classes.tif")
    output_png = os.path.join(output_dir, f"{output_prefix}_rgb.png")

    print(f"📥 Lendo arquivo NDVI: {ndvi_path}")
    with rasterio.open(ndvi_path) as src:
        ndvi_array = src.read(1)
        profile = src.profile.copy()
        transform, crs = src.transform, src.crs
        ndvi_array = np.nan_to_num(ndvi_array)

    print("⚖️ Normalizando NDVI...")
    ndvi_array = normalize_ndvi(ndvi_array)

    print("🤖 Rodando predição na imagem completa...")
    predicted_mask, rgba_image = predict_full_image(ndvi_array, model_path, tile_size, stride)

    profile.pop("nodata", None)
    profile.update(dtype=rasterio.uint8, count=1)

    print(f"💾 Salvando máscara raster em: {output_tif}")
    with rasterio.open(output_tif, "w", **profile) as dst:
        dst.write(predicted_mask, 1)

    print(f"🖼️ Salvando imagem RGB com classes: {output_png}")
    rgba_image.save(output_png)

    return output_tif, output_png

def normalize_ndvi(ndvi):
    if ndvi.min() < 0 or ndvi.max() > 1:
        print("📐 NDVI fora do intervalo [0, 1], aplicando normalização.")
        return (ndvi + 1) / 2
    return ndvi

def predict_full_image(ndvi, model_path, tile_size, stride):
    h, w = ndvi.shape
    print(f"📏 Dimensões da imagem: {h} x {w}")
    model = load_model(model_path)
    predicted_mask = np.zeros((h, w), dtype=np.uint8)
    rgba_image = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(rgba_image)

    print("🔄 Modelo carregado, iniciando varredura por tiles...")

    # Calcular total de tiles
    num_tiles_y = (h - 1) // stride + 1
    num_tiles_x = (w - 1) // stride + 1
    total_tiles = num_tiles_y * num_tiles_x
    current_tile = 0

    with torch.no_grad():
        for i in range(0, h, stride):
            for j in range(0, w, stride):
                current_tile += 1
                i_end, j_end = min(i + tile_size, h), min(j + tile_size, w)
                tile = ndvi[i:i_end, j:j_end]
                tile_padded = np.pad(tile, ((0, tile_size - tile.shape[0]), (0, tile_size - tile.shape[1])), mode='constant')

                # Progresso
                porcentagem = (current_tile / total_tiles) * 100
                print(f"🧩 Tile {current_tile}/{total_tiles} ({porcentagem:.2f}%) — Área: ({i}:{i_end}, {j}:{j_end}) Tamanho: {tile.shape}")

                tensor = torch.tensor(tile_padded, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to("cuda" if torch.cuda.is_available() else "cpu")
                output = model(tensor).squeeze(0).cpu().numpy()[:, :tile.shape[0], :tile.shape[1]]
                predicted = np.argmax(output, axis=0).astype(np.uint8)
                predicted_mask[i:i_end, j:j_end] = predicted

                # Log das classes detectadas
                classes_presentes = np.unique(predicted)
                print(f"📊 Classes detectadas: {classes_presentes.tolist()}")

                for label, color in COLORS.items():
                    ys, xs = np.where(predicted == label)
                    for y, x in zip(ys, xs):
                        draw.point((j + x, i + y), fill=color)

    print("✅ Predição finalizada.")
    return predicted_mask, rgba_image

def load_model(path):
    print(f"📦 Carregando modelo de: {path}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = get_unet_model(num_classes=4).to(device)
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    print("✅ Modelo carregado e em modo de avaliação.")
    return model
