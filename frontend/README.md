# T2S Hackathon Frontend

Este projeto utiliza React para criar a interface web do portal de avaliação automatizada.

## Como iniciar

1. Instale o Node.js e o npm (https://nodejs.org/)
2. Execute os comandos:
   ```bash
   npm install
   npm start
   ```

## Estrutura sugerida
- `src/`
  - `App.js` — Componente principal
  - `components/` — Componentes do dashboard, formulário, ranking, relatório
  - `services/` — Integração com API FastAPI

## Funcionalidades
- Submissão de URLs de repositórios
- Visualização do status das análises
- Exibição de ranking e relatórios em Markdown

## Observação
Este frontend está pronto para integração com o backend FastAPI.

## Observação sobre o repositório
O diretório `node_modules` e arquivos de build não são enviados para o GitHub, pois estão listados no arquivo `.gitignore`. Após clonar o projeto, execute `npm install` para instalar todas as dependências necessárias.
