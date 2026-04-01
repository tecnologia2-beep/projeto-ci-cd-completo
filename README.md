# Projeto CI/CD - Geração de Código Sequencial

## Tecnologias
- Python
- Flask
- MySQL
- Pytest
- Docker
- GitHub Actions
- GHCR

## O que este projeto faz
- Gera código sequencial de produtos
- Expõe uma API HTTP com Flask
- Executa testes automatizados no pipeline
- Publica imagem Docker no GitHub Container Registry
- Faz deploy automático em servidor Linux via SSH

## Endpoints
### Healthcheck
```bash
GET /health
```

### Criar produto
```bash
POST /produtos
Content-Type: application/json

{
  "grupo": "C",
  "tipo_alimento": "A",
  "pais": "BR"
}
```

## Execução local com Docker
```bash
docker compose up -d --build
```

API disponível em:
```bash
http://localhost:5000
```

## Execução local sem Docker
```bash
pip install -r requirements.txt
python app.py
```

## Secrets necessários no GitHub
Para o deploy automático em servidor Linux, configure estes secrets no repositório:

- `SSH_HOST`
- `SSH_USER`
- `SSH_PRIVATE_KEY`
- `MYSQL_ROOT_PASSWORD`
- `MYSQL_DATABASE`

## Fluxo do pipeline
1. Executa testes automatizados
2. Sobe a API e roda smoke test
3. Gera imagem Docker
4. Publica no GHCR
5. Faz deploy automático no servidor
