import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
import rasterio
import requests
import os
from tempfile import NamedTemporaryFile

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.segmentation.deeplabv3_resnet50(weights="DEFAULT")
model.eval().to(device)

preprocess = transforms.Compose([
    transforms.Resize(520),
    transforms.CenterCrop(512),
    transforms.ToTensor()
])

def download_band(url: str) -> np.ndarray:
    response = requests.get(url)
    response.raise_for_status()
    with NamedTemporaryFile(delete=False, suffix=".tif") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    with rasterio.open(tmp_path) as src:
        data = src.read(1).astype("float32")
    os.remove(tmp_path)
    return data

def run_rgb_segmentation(band13_url: str, band15_url: str, band16_url: str, output_path: str = "masks/segment_rgb.png") -> str:
    b = download_band(band13_url)
    g = download_band(band15_url)
    r = download_band(band16_url)

    stacked = np.stack([r, g, b], axis=-1)  # shape: (H, W, 3)
    stacked = np.nan_to_num(stacked, nan=0.0)

    # Normalização simples para [0, 255]
    norm = (stacked - stacked.min()) / (stacked.max() - stacked.min())
    image_uint8 = (norm * 255).astype("uint8")
    img = Image.fromarray(image_uint8)

    input_tensor = preprocess(img).unsqueeze(0).to(device) # type: ignore

    with torch.no_grad():
        output = model(input_tensor)['out'][0]
        prediction = torch.argmax(output, dim=0).cpu().numpy()

    # Classe 15 = vegetação
    mask_array = (prediction == 15).astype("uint8") * 255
    mask = Image.fromarray(mask_array)
    os.makedirs("masks", exist_ok=True)
    mask.save(output_path)

    return output_path
