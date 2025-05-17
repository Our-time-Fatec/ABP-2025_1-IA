import requests
import os
from typing import Optional
from PIL import Image
import io

# Permite imagens grandes (acima de ~170 MP). Útil se você confiar na origem da imagem.
Image.MAX_IMAGE_PIXELS = None

def comprimir_imagem(imagem_path: str, qualidade: int = 70, max_lado: int = 1024) -> io.BytesIO:
    """Comprime a imagem redimensionando e salvando em JPEG."""
    img = Image.open(imagem_path)
    img = img.convert("RGB")  # Garante que está no modo compatível com JPEG

    # Redimensiona a imagem, mantendo a proporção
    img.thumbnail((max_lado, max_lado))

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG", quality=qualidade, optimize=True)
    img_bytes.seek(0)
    return img_bytes

def enviar_imagem_para_servico(destino_url: str, imagem_path: str, dados_extra: Optional[dict] = None):
    print(f"🚀 Enviando imagem para {destino_url}...")

    imagem_comprimida = comprimir_imagem(imagem_path)

    files = {
        "file": (
            os.path.splitext(os.path.basename(imagem_path))[0] + ".jpg",
            imagem_comprimida,
            "image/jpeg"
        )
    }

    response = requests.post(
        destino_url,
        data=dados_extra or {},
        files=files,
        timeout=30  
    )

    print(f"📬 Resposta do serviço: {response.status_code} - {response.text}")
    return response
