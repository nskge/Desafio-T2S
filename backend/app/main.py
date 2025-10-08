import os
import uuid
import json
import requests
from typing import Dict, Literal
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from huggingface_hub import InferenceClient

# --- Configuração do Cliente Hugging Face ---
token = os.getenv("HF_TOKEN")
if not token:
    raise RuntimeError("A variável de ambiente HF_TOKEN não foi definida.")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=token
)

# --- Modelos de Dados (Contrato da API) ---
class RepoSubmission(BaseModel):
    repo_url: str = Field(..., example="https://github.com/exemplo/projeto")

class TaskStatus(BaseModel):
    task_id: str
    status: Literal["PENDING", "IN_PROGRESS", "SUCCESS", "FAILURE"]
    message: str
    result: dict | None = None

# --- Simulação de Banco de Dados ---
tasks_db: Dict[str, TaskStatus] = {}

# --- LÓGICA DE ANÁLISE REAL COM HUGGING FACE ---
def perform_real_analysis(task_id: str, repo_url: str):
    print(f"Iniciando análise REAL com HUGGING FACE para a task {task_id}")
    
    tasks_db[task_id].status = "IN_PROGRESS"
    tasks_db[task_id].message = "Buscando README.md do repositório..."

    readme_content = None

    try:
        parts = repo_url.replace("https://github.com/", "").split("/")
        user = parts[0]
        repo = parts[1]
        
        urls_to_try = [
            f"https://raw.githubusercontent.com/{user}/{repo}/main/README.md",
            f"https://raw.githubusercontent.com/{user}/{repo}/master/README.md"
        ]
        
        for url in urls_to_try:
            response = requests.get(url)
            if response.status_code == 200:
                if response.text.strip():
                    readme_content = response.text
                    break
        
        if readme_content:
            tasks_db[task_id].message = "README.md encontrado! Analisando com a IA..."
            if len(readme_content) > 4000:
                readme_content = readme_content[:4000]

            prompt_content = f"""Você é um engenheiro de software sênior.
            Analise o seguinte arquivo README.md de um projeto de software e atribua uma pontuação de qualidade de 0.0 a 10.0.
            Considere clareza, completude das instruções e profissionalismo.

            Conteúdo do README.md:
            ---
            {readme_content}
            ---

            Sua resposta DEVE SER APENAS um objeto JSON válido, sem nenhum texto adicional.
            O JSON deve ter a seguinte estrutura:
            {{
              "repo_url": "{repo_url}",
              "overall_score": <sua_pontuação_numerica>,
              "summary": "<uma justificativa curta para a sua pontuação baseada no README>"
            }}
            """
        else:
            tasks_db[task_id].message = "README.md não encontrado ou vazio. Avaliando com base na ausência de documentação..."
            prompt_content = f"""Você é um engenheiro de software sênior.
            A análise de um projeto na URL '{repo_url}' falhou em encontrar um arquivo README.md ou encontrou um README vazio.
            A ausência de documentação é uma falha grave de engenharia de software.

            Baseado exclusivamente nesta informação, atribua uma pontuação de qualidade. A nota deve ser muito baixa (entre 0.0 e 2.0).

            Sua resposta DEVE SER APENAS um objeto JSON válido, sem nenhum texto adicional.
            O JSON deve ter a seguinte estrutura:
            {{
              "repo_url": "{repo_url}",
              "overall_score": <sua_pontuação_numerica_baixa>,
              "summary": "A pontuação é extremamente baixa porque o projeto não possui um arquivo README.md ou ele está vazio."
            }}
            """

        messages = [{"role": "user", "content": prompt_content}]

        # --- Chamada para a API de Inferência ---
        response_chat = client.chat_completion(
            messages=messages,
            max_tokens=500,
            temperature=0.1 # <-- ADICIONAMOS ESTE PARÂMETRO PARA FORÇAR CONSISTÊNCIA
        )
        
        response_text = response_chat.choices[0].message.content
        
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start != -1 and json_end != -1:
            json_str = response_text[json_start:json_end]
            result_json = json.loads(json_str)
        else:
            raise ValueError("A resposta da IA não continha um JSON válido.")

        tasks_db[task_id].status = "SUCCESS"
        tasks_db[task_id].message = "Análise concluída com sucesso!"
        tasks_db[task_id].result = result_json
        print(f"Análise da task {task_id} concluída.")

    except Exception as e:
        print(f"ERRO durante a análise da task {task_id}: {e}")
        tasks_db[task_id].status = "FAILURE"
        tasks_db[task_id].message = f"Ocorreu um erro: {e}"

# --- Aplicação FastAPI (continua igual) ---
app = FastAPI(title="DevReview AI")

@app.post("/api/analyze", response_model=TaskStatus, status_code=202)
def start_analysis(submission: RepoSubmission, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    initial_status = TaskStatus(
        task_id=task_id, status="PENDING", message="Análise agendada."
    )
    tasks_db[task_id] = initial_status
    background_tasks.add_task(perform_real_analysis, task_id, submission.repo_url)
    return initial_status

@app.get("/api/status/{task_id}", response_model=TaskStatus)
def get_task_status(task_id: str):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada.")
    return task