# StudentRegister

<p align="center">
	<img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" />
	<img src="https://img.shields.io/badge/FastAPI-0.135-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
	<img src="https://img.shields.io/badge/Uvicorn-Server-2B2B2B?style=for-the-badge&logo=uvicorn&logoColor=white" />
	<img src="https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white" />
	<img src="https://img.shields.io/badge/PostgreSQL-asyncpg-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
	<img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
	<img src="https://img.shields.io/badge/Pytest-9.0-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
</p>

API REST desenvolvida com FastAPI para gerenciamento de alunos. Este projeto demonstra uma estrutura de diretórios escalável e boas práticas de qualidade de software com testes isolados.

- Rotas organizadas por responsabilidade (Alunos)
- Modelo de domínio e validação de dados com Pydantic
- Separação de camadas (Rotas, Schemas (DTO) e Serviços)
- Persistência assíncrona com PostgreSQL via `asyncpg`
- Middlewares HTTP para log e modificação de resposta (headers customizados)
- Execução local e via Docker (com docker-compose)
- Testes de integração com `pytest` sem dependência de banco real (mock in-memory)

## Visão Geral

Este repositório foi organizado para servir como demonstração de uma aplicação FastAPI estruturada com qualidade de produção, com suporte integrado para testes e containerização.

O fluxo principal é:

1. A aplicação recebe a requisição em `main.py`.
2. As requisições passam pelos middlewares, que registram o log das chamadas HTTP e adicionam cabeçalhos de controle.
3. As rotas em `app/routes/student.py` interceptam a requisição e chamam os métodos de negócio correspondentes na camada de serviço.
4. Os dados são validados pelos modelos Pydantic localizados na pasta `schemas`.
5. O serviço persiste e consulta os dados via conexão assíncrona com o PostgreSQL (`asyncpg`).

## Stack

- Python 3.13
- FastAPI 0.135
- Uvicorn
- Pydantic
- asyncpg (PostgreSQL)
- Pytest + pytest-asyncio
- Docker / Docker Compose

## Estrutura do Projeto

```text
StudentRegister/
├── app/
│   ├── db/
│   │   ├── connection.py
│   │   └── init.sql
│   ├── middlewares/
│   │   ├── custom_header.py
│   │   └── logging.py
│   ├── routes/
│   │   └── student.py
│   ├── schemas/
│   │   └── student.py
│   └── services/
│       └── student_service.py
├── test/
│   ├── conftest.py
│   └── test_api.py
├── main.py
├── requirements.txt
├── pytest.ini
├── .env.example
├── Dockerfile
└── docker-compose.yaml
```

### Responsabilidade dos arquivos

- `main.py`: Ponto de entrada da aplicação FastAPI e setup da documentação autogerada (Swagger).
- `app/db/connection.py`: Fábrica de conexão assíncrona com o PostgreSQL via `asyncpg`.
- `app/db/init.sql`: Script de inicialização do schema do banco de dados.
- `app/routes/student.py`: Endpoints relacionados à entidade de aluno (Alunos CRUD).
- `app/middlewares/`: Arquivos que integram processamento a cada requisição (logs, marcação de tempos e alteração de headers).
- `app/schemas/student.py`: Estruturas Pydantic (`Student`, `StudentCreate`, `StudentUpdate`) para representação e validação de corpo.
- `app/services/student_service.py`: Classe encarregada pela lógica de negócio e persistência dos alunos.
- `test/conftest.py`: Fixtures compartilhadas entre os testes — inclui mock da conexão com banco e reset de estado entre execuções.
- `test/test_api.py`: Suítes de teste de integração para todos os endpoints.
- `Dockerfile` e `docker-compose.yaml`: Configuração via Docker para empacotar a aplicação e o banco de dados de maneira reproduzível.

## Configuração

Copie o arquivo de exemplo e preencha as variáveis:

```bash
cp .env.example .env
```

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | String de conexão com o PostgreSQL | `postgresql://user:pass@localhost:5432/students` |

## Executando

### Com Docker Compose

```bash
docker-compose up --build
```

A API ficará disponível em `http://localhost:8000`.

### Localmente (sem Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

> Certifique-se de ter o PostgreSQL rodando e o `DATABASE_URL` configurado no `.env`.

## Testes

Os testes rodam **sem necessidade de banco de dados real**. A conexão com o PostgreSQL é substituída por um mock in-memory via `unittest.mock.patch`, garantindo isolamento e velocidade.

```bash
pytest test/ -v
```

Cada teste parte de um estado limpo: o banco fake é resetado antes e após cada execução via fixture `autouse`.

## Middlewares

O projeto demonstra o uso de middlewares no framework:

- **Logging Middleware** (`logging.py`): Intercepta e informa no terminal detalhes das requisições entrantes e respostas prontas junto com o tempo total de processamento no back-end.
- **Custom Header Middleware** (`custom_header.py`): Adiciona o header `X-App-Version: 1.0` de forma padronizada nas respostas tratadas pelo serviço.

## Endpoints

### Healthcheck

`GET /`

Retorna o status verificando a disponibilidade.

#### Resposta

```json
{
	"message": "API is running! 🚀"
}
```

### Alunos

Toda a gestão fica restrita a `prefix="/api/v1/alunos"`.

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/v1/alunos/` | Cria um novo aluno |
| `GET` | `/api/v1/alunos/` | Lista todos os alunos |
| `GET` | `/api/v1/alunos/{student_id}` | Recupera um aluno pelo ID |
| `PATCH` | `/api/v1/alunos/{student_id}` | Atualiza parcialmente um aluno |
| `DELETE` | `/api/v1/alunos/{student_id}` | Remove um aluno |
| `DELETE` | `/api/v1/alunos/` | Remove todos os alunos (reset) |

A documentação interativa completa está disponível em `/docs` (Swagger UI) e `/redoc`.
