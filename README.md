# 🌿 Treinamento de IA da ABP

Projeto de Análise de Imagens Satelitais com Inferência de IA, voltado ao processamento e extração de índices como NDVI, segmentação de imagens RGB e inferência com modelos de deep learning. Desenvolvido como parte do ABP (Aprendizagem Baseada em Projetos) da FATEC Jacareí.

## 📁 Estrutura do Projeto

```
ABP-2025_1-IA/
├─ app/
│  ├─ api/                  # Rotas da API FastAPI
│  ├─ controllers/          # Lógicas principais para upload, inferência, segmentação
│  ├─ models/               # Modelos treinados (.pth)
│  ├─ schemas/              # Schemas Pydantic
│  ├─ services/             # Processamentos de imagem e execução de pipeline
│  ├─ utils/                # Utilitários diversos
│  └─ main.py               # Ponto de entrada da aplicação FastAPI
├─ logs/                    # Logs e resultados de inferência
├─ .gitignore
├─ requirements.txt         # Dependências do projeto
```

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Our-time-Fatec/ABP-2025_1-IA.git
cd ABP-2025_1-IA
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a API

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📡 Endpoints Principais

| Método | Rota      | Descrição                                   |
| ------ | --------- | ------------------------------------------- |
| GET    | `/status` | Verifica o status da aplicação              |
| POST   | `/nvdi/v3`   | Processa uma imagem e retorna a imagem processada e todos seus dados de analytics |

Documentação Swagger disponível em:
`http://127.0.0.1:8000/docs`

## 🧠 Modelos de IA

Localizados em `app/models/`:

* `final_model_1.pth`
* `final_model_treino_novo.pth`

Usados para segmentação de imagens satelitais e RGB com redes neurais profundas (PyTorch + segmentation-models-pytorch).

## 📊 Logs e Resultados

Todos os resultados processados são salvos na pasta `logs/` como arquivos `.json`, com informações sobre a imagem, tempo de execução, parâmetros e resultados.

## 🛠 Tecnologias Utilizadas

* **FastAPI** — Backend leve e performático
* **PyTorch** — Treinamento e inferência de modelos
* **rasterio** — Leitura de imagens satelitais
* **Pillow** — Manipulação de imagens
* **matplotlib** — Geração de visualizações
* **pyproj** — Projeções geográficas

## 📌 Contribuições

Sinta-se livre para abrir *Issues* e *Pull Requests*. Toda contribuição é bem-vinda!

## 📜 Licença

Este projeto é acadêmico e de uso educacional. Direitos reservados aos integrantes do grupo DaVinci Codes.
