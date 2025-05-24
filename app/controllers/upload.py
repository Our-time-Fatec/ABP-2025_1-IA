import requests
import os
from typing import Optional
from PIL import Image
import io

Image.MAX_IMAGE_PIXELS = None

def comprimir_imagem(imagem_path: str, qualidade: int = 70, max_lado: int = 1024) -> io.BytesIO:
    img = Image.open(imagem_path)
    img = img.convert("RGB")
    img.thumbnail((max_lado, max_lado))

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG", quality=qualidade, optimize=True)
    img_bytes.seek(0)
    return img_bytes

async def enviar_imagem_para_servico(
    destino_url: str,
    imagem_path: str,
    dados_extra: Optional[dict] = None,  # Estes campos virarão campos do formulário
    query_params: Optional[dict] = None,
    headers=None
) -> requests.Response:
    print(f"🚀 Enviando imagem para {destino_url}...")

    imagem_comprimida = comprimir_imagem(imagem_path)

    files = {
        "file": (
            os.path.splitext(os.path.basename(imagem_path))[0] + ".jpg",
            imagem_comprimida,
            "image/jpeg"
        )
    }
    
    print(dados_extra)

    response = requests.post(
        destino_url,
        json=dados_extra,   # ← campos de formulário além do arquivo (ex: jobId, status)
        files=files,
        params=query_params,
        headers=headers
    )

    print(f"📬 Resposta do serviço: {response.status_code} - {response.text}")
    return response

async def enviar_dados_para_servico(
    destino_url: str,
    dados_extra: Optional[dict] = None,  # Campos do formulário
    query_params: Optional[dict] = None,
    headers=None
) -> requests.Response:
    print(f"🚀 Enviando dados para {destino_url}...")
    
    print(dados_extra)

    response = requests.post(
        destino_url,
        json=dados_extra, 
        params=query_params,
        headers=headers
    )

    print(f"📬 Resposta do serviço: {response.status_code} - {response.text}")
    return response
