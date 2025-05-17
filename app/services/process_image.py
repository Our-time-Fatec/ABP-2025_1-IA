from app.schemas.schemas import MLProcessRequest
from app.services.process.pipeline import processar_imagem_completa
from app.controllers.upload import enviar_imagem_para_servico

async def process_upload_image(data: MLProcessRequest) -> dict:
    result = await processar_imagem_completa(data)

    # 🔁 Após pipeline, envie a imagem para outro serviço
    destino_url = "http://localhost:3030/upload"
    caminho_da_imagem = f"output/{data.id}_rgb.png"

    dados = {
        "id": data.id,
        "bbox_real": ",".join(map(str, result["bbox_real"])),
        "bbox": ",".join(map(str, result["bbox"])),
    }

    try:
        resposta = enviar_imagem_para_servico(destino_url, caminho_da_imagem, dados)
        response_info = {
            "status_code": resposta.status_code,
            "resposta_texto": resposta.text
        }
    except Exception as e:
        print(f"❌ Falha ao enviar imagem para {destino_url}: {e}")
        response_info = {
            "status_code": None,
            "erro": str(e)
        }

    return {
        "resultados_pipeline": result,
        "resposta_envio": response_info
    }
