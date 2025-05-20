# Projeto: Scraper com Inferência de Imagem - AXUR

Este projeto realiza:

1. Scraping de uma imagem codificada em base64 a partir de uma URL.
2. Salva a imagem em uma pasta.
3. Envia a imagem para inferência no modelo `microsoft-florence-2-large`.
4. Submissão da resposta da inferência para uma API.

## Requisitos

* Docker

## Como usar

### 1. Clone o projeto

```bash
git clone https://github.com/miraceli/axur.git
cd axur
```

### 2. Crie o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
URL=https://intern.aiaxuropenings.com/scrape/0a696940-9bf3-4579-8b52-732284ff7720
TOKEN=sua_token_aqui
API_URL=https://intern.aiaxuropenings.com/v1/chat/completions
SUBMIT_URL=https://intern.aiaxuropenings.com/api/submit-response
```

### 3. Execute o projeto com Docker

```bash
docker compose up --build
```

A imagem será salva na pasta `images/`, o resultado da inferência será exibido no terminal e enviado automaticamente para a API de submissão.

## Estrutura de Arquivos

```
axur/
├── Dockerfile                # Define a imagem Docker
├── docker-compose.yml        # Orquestra o container com variáveis de ambiente
├── scrap.py                  # Script principal
├── read_env_var.py           # Carrega as variáveis de ambiente
├── requirements.req          # Lista de dependências Python
├── .env                      # Variáveis de ambiente (não incluído no repositório)
└── images/                   # Pasta onde as imagens são salvas
```

## Observação

O uso de Docker elimina a necessidade de instalar dependências Python localmente ou configurar ambientes virtuais.
