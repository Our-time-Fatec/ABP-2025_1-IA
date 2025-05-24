import json
import os
from app.schemas.schemas import MLProcessRequest
from app.controllers.upload import enviar_imagem_para_servico, enviar_dados_para_servico
from app.services.job_manager import job_manager

async def process_upload_image_mock(data: MLProcessRequest, job_id: str) -> dict:
    # 🧪 Carregar resultado mock
    with open("logs/result.json", "r", encoding="utf-8") as f:
        result = json.load(f)

    # 🔁 Atualizar status no job manager
    job_manager.update_job(job_id, "completed", result)
    job_info = job_manager.get_job(job_id)
    if not job_info:
        raise ValueError(f"Job with id {job_id} not found.")
    status = job_info["status"]

    destino_url = "http://localhost:3030/cicatriz/test"
    dados_url = "http://localhost:3030/cicatriz/test"
    
    query_params = {
        "jobId": job_id,
        "status": status
    }
    headers = {
        "Authorization": f"Bearer {data.JWT}"
    }

    caminho_da_imagem = f"output/3_rgb.png"
    dados_extra = {"jobId": "12345", "status": "success"}
    
    try:
        resposta = await enviar_dados_para_servico(dados_url, result, query_params, headers)  
        # resposta1 = enviar_imagem_para_servico(destino_url, caminho_da_imagem, dados_extra, query_params, headers)
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

    # 💾 Salvar resultado completo simulado
    resultado_completo = {
        "id": data.id,
        "job_id": job_id,
        "status": status,
        "resultados_pipeline": result,
        "resposta_envio": response_info
    }


    return resultado_completo
