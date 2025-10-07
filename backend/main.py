# FastAPI backend for T2S Hackathon

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="T2S Hackathon Backend")

# Models
class RepoSubmission(BaseModel):
    urls: List[str]

class CriterionScore(BaseModel):
    name: str
    score: float
    justification: str

class AnalysisStatus(BaseModel):
    repo_url: str
    status: str
    total_score: Optional[float] = None
    criteria: Optional[List[CriterionScore]] = None
    report: Optional[str] = None

# In-memory store (for prototype)
analysis_db = {}

# Endpoints
@app.post("/submit", response_model=List[AnalysisStatus])
def submit_repos(submission: RepoSubmission, background_tasks: BackgroundTasks):
    results = []
    for url in submission.urls:
        analysis_db[url] = {"status": "pending"}
        background_tasks.add_task(analyze_repo, url)
        results.append(AnalysisStatus(repo_url=url, status="pending"))
    return results

@app.get("/status/{repo_url}", response_model=AnalysisStatus)
def get_status(repo_url: str):
    data = analysis_db.get(repo_url)
    if not data:
        return AnalysisStatus(repo_url=repo_url, status="not_found")
    return AnalysisStatus(
        repo_url=repo_url,
        status=data["status"],
        total_score=data.get("total_score"),
        criteria=data.get("criteria"),
        report=data.get("report")
    )

@app.get("/report/{repo_url}", response_model=AnalysisStatus)
def get_report(repo_url: str):
    data = analysis_db.get(repo_url)
    if not data or "report" not in data:
        return AnalysisStatus(repo_url=repo_url, status="not_found")
    return AnalysisStatus(
        repo_url=repo_url,
        status=data["status"],
        total_score=data.get("total_score"),
        criteria=data.get("criteria"),
        report=data.get("report")
    )

# Endpoint para ranking
@app.get("/ranking", response_model=List[AnalysisStatus])
def get_ranking():
    # Retorna todos os projetos avaliados, ordenados por pontuação
    ranked = [
        AnalysisStatus(
            repo_url=k,
            status=v["status"],
            total_score=v.get("total_score"),
            criteria=v.get("criteria"),
            report=v.get("report")
        )
        for k, v in analysis_db.items() if v["status"] == "done"
    ]
    ranked.sort(key=lambda x: x.total_score or 0, reverse=True)
    return ranked

# Dummy analysis function
import time

def analyze_repo(repo_url: str):
    time.sleep(2)  # Simulate analysis
    # Critérios simulados
    criteria = [
        CriterionScore(name="Adequação Funcional", score=16, justification="README.md presente e coerente."),
        CriterionScore(name="Manutenibilidade", score=16, justification="Código claro e comentado."),
        CriterionScore(name="Confiabilidade", score=16, justification="Testes automatizados detectados."),
        CriterionScore(name="Usabilidade", score=16, justification="Documentação completa."),
        CriterionScore(name="Desempenho", score=16, justification="Execução rápida e eficiente."),
        CriterionScore(name="Origem e Tratamento dos Dados", score=10, justification="Dados bem tratados."),
        CriterionScore(name="Técnicas Aplicadas", score=10, justification="Técnicas de IA identificadas."),
        CriterionScore(name="Validação e Escolha de Modelos", score=10, justification="Justificativa de escolha do modelo presente."),
        CriterionScore(name="Métricas, Custo e Desempenho", score=10, justification="Métricas e custo analisados."),
        CriterionScore(name="Segurança e Governança", score=10, justification="Riscos e guardrails implementados.")
    ]
    total_score = sum(c.score for c in criteria)
    report_md = f"# Relatório de Análise\n\nProjeto: {repo_url}\nPontuação Total: {total_score}/130\n\n## Critérios\n" + "\n".join([
        f"### {c.name}\nPontuação: {c.score}\nJustificativa: {c.justification}" for c in criteria
    ])
    analysis_db[repo_url] = {
        "status": "done",
        "total_score": total_score,
        "criteria": criteria,
        "report": report_md
    }
