# T2S Hackathon Backend

FastAPI backend para avaliação automatizada de projetos de software com IA.

## Como executar

1. Instale as dependências:
   ```bash
   pip install fastapi uvicorn
   ```
2. Execute o servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints
- `POST /submit` — Submete URLs de repositórios para análise
- `GET /status/{repo_url}` — Consulta status da análise
- `GET /report/{repo_url}` — Obtém relatório em Markdown
- `GET /ranking` — Lista projetos avaliados em ordem de pontuação

## Estrutura
- `main.py` — API principal

## Observação
Este backend está pronto para integração futura com motor de IA e frontend React.

## Observação sobre o repositório
O diretório `.venv`, arquivos de cache e variáveis de ambiente não são enviados para o GitHub, pois estão listados no arquivo `.gitignore`. Após clonar o projeto, crie e ative um ambiente virtual e instale as dependências com `pip install -r requirements.txt` ou conforme instruções acima.
