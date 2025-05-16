from pydantic import BaseModel
from typing import List

class ImageInput(BaseModel):
    url: str

class NDVIInput(BaseModel):
    red_url: str   # URL da BAND13
    nir_url: str   # URL da BAND14

class RGBInput(BaseModel):
    band13_url: str  # usado como Blue
    band15_url: str  # usado como Green
    band16_url: str  # usado como Red

class MLProcessRequest(BaseModel):
    id: str
    band15_url: str
    band16_url: str
    bbox: List[float]  # [lon_min, lat_min, lon_max, lat_max]