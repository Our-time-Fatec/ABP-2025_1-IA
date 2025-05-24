import json
import os
from app.schemas.schemas import MLProcessRequest
from app.services.process.pipeline import processar_imagem_completa
from app.controllers.upload import enviar_imagem_para_servico, enviar_dados_para_servico
from app.services.job_manager import job_manager

async def process_upload_image(data: MLProcessRequest, job_id: str) -> dict:
    result = await processar_imagem_completa(data)  # NDVI + geração de imagem

    # 🔁 Consultar status atual
    job_manager.update_job(job_id, "completed", result)
    job_info = job_manager.get_job(job_id)
    if not job_info:
        raise ValueError(f"Job with id {job_id} not found.")
    status = job_info["status"]

    destino_url = "http://localhost:3030/cicatriz/finalize"
    dados_url = "http://localhost:3030/analytics/save-analytics"
    
    query_params = {
        "jobId": job_id,
        "status": status
    }
    
    headers = {
        "Authorization": f"Bearer {data.JWT}"
    }

    caminho_da_imagem = f"output/{data.id}_rgb.png"
    dados = {
        "id": data.id,
        "bbox_real": ",".join(list(map(str, result.get("bbox_real", [])))),
        "bbox": ",".join(map(str, result.get("bbox", []))),
    }

    try:
        resposta = await enviar_imagem_para_servico(destino_url, caminho_da_imagem, dados, query_params, headers)
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
        
    try:
            resposta = await enviar_dados_para_servico(dados_url, result, query_params, headers)
            response_info2 = {
                "status_code": resposta.status_code,
                "resposta_texto": resposta.text
            }
    except Exception as e:
            print(f"❌ Falha ao enviar dados para {dados_url}: {e}")
            response_info2 = {
                "status_code": None,
                "erro": str(e)
            }

    # 💾 Salvar resultado no .json
    resultado_completo = {
        "id": data.id,
        "job_id": job_id,
        "status": status,
        "resultados_pipeline": result,
        "resposta_envio": response_info,
        "resposta_envio_dados": response_info2
    }

    # os.makedirs("logs", exist_ok=True)
    # with open(f"logs/resultados_{data.id}.json", "w", encoding="utf-8") as f:
    #     json.dump(resultado_completo, f, indent=2, ensure_ascii=False)

    return resultado_completo
