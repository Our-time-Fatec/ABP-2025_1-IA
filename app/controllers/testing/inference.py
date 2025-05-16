import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
import rasterio
import os
import requests
from io import BytesIO
from tempfile import NamedTemporaryFile

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.segmentation.deeplabv3_resnet50(weights="DEFAULT")
model.eval().to(device)

preprocess = transforms.Compose([
    transforms.Resize(520),
    transforms.CenterCrop(512),
    transforms.ToTensor()
])

def download_image(url: str) -> str:
    """Baixa uma imagem COG para um arquivo temporário local"""
    response = requests.get(url)
    response.raise_for_status()
    tmp = NamedTemporaryFile(delete=False, suffix=".tif")
    tmp.write(response.content)
    tmp.close()
    return tmp.name

def extract_rgb_like_tensor(image_path: str) -> torch.Tensor:
    """Carrega bandas 3, 2, 1 (R, G, B) de um COG como tensor PyTorch normalizado"""
    with rasterio.open(image_path) as src:
        # As bandas podem variar por sensor — ajuste conforme necessário
        red = src.read(3).astype("float32")
        green = src.read(2).astype("float32")
        blue = src.read(1).astype("float32")

        # Normaliza valores para 0-255 e cria imagem PIL
        stacked = np.stack([red, green, blue], axis=-1)
        stacked = np.nan_to_num(stacked, nan=0.0)

        # Normalização simples para converter em uint8 (pode ser ajustado)
        norm = (stacked - stacked.min()) / (stacked.max() - stacked.min())
        image_uint8 = (norm * 255).astype("uint8")

        pil_image = Image.fromarray(image_uint8)
        return preprocess(pil_image) # type: ignore

def run_inference_from_cog_url(url: str, output_path: str = "masks/mask_from_cog.png") -> str:
    os.makedirs("masks", exist_ok=True)

    local_path = download_image(url)
    input_tensor = extract_rgb_like_tensor(local_path).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)["out"][0]
        prediction = torch.argmax(output, dim=0).cpu().numpy()

    # Exemplo: 15 = vegetação
    mask_array = (prediction == 15).astype("uint8") * 255
    mask = Image.fromarray(mask_array)
    mask.save(output_path)

    os.remove(local_path)
    return output_path
