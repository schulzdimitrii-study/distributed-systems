# StudentRegister

<p align="center">
	<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" />
	<img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
	<img src="https://img.shields.io/badge/Uvicorn-Server-2B2B2B?style=for-the-badge&logo=uvicorn&logoColor=white" />
	<img src="https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white" />
	<img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

API REST desenvolvida com FastAPI para gerenciamento de alunos. Este projeto demonstra uma estrutura de diretórios escalável para API e implementação de testes.

- Rotas organizadas por responsabilidade (Alunos)
- Modelo de domínio e validação de dados com Pydantic
- Separação de camadas (Rotas, Schemas (DTO) e Serviços)
- Middlewares HTTP para log e modificação de resposta (headers customizados)
- Execução local e via Docker (com docker-compose)
- Ambiente voltado a testes integrados com `pytest`

O projeto utiliza armazenamento em memória, por isso os dados são perdidos quando a aplicação reinicia.

## Visão Geral

Este repositório foi organizado para servir como demonstração de uma aplicação FastAPI estruturada com qualidade de produção, com suporte integrado para testes e containerização.

O fluxo principal é:

1. A aplicação recebe a requisição em `main.py`.
2. As requisições passam pelos middlewares, que registram o log das chamadas HTTP e adicionam cabeçalhos de controle.
3. As rotas em `app/routes/student.py` interceptam a requisição e chamam os métodos de negócio correspondentes na camada de serviço.
4. Os dados são validados pelos modelos Pydantic localizados na pasta `schemas`.

## Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- Docker

## Estrutura do Projeto

```text
StudentRegister/
├── app/
│   ├── middlewares/
│   │   ├── custom_header.py
│   │   └── logging.py
│   ├── routes/
│   │   └── student.py
│   ├── schemas/
│   │   └── student.py
│   └── services/
│       └── studentService.py
├── test/
│   └── test_api.py
├── main.py
├── requirements.txt
├── pytest.ini
├── Dockerfile
└── docker-compose.yaml
```

### Responsabilidade dos arquivos

- `main.py`: Ponto de entrada da aplicação FastAPI e setup da documentação autogerada (Swagger).
- `app/routes/student.py`: Endpoints relacionados à entidade de aluno (Alunos CRUD).
- `app/middlewares/`: Arquivos que integram processamento a cada requisição (logs, marcação de tempos e alteração de headers).
- `app/schemas/student.py`: Estruturas Pydantic (`Student`, `StudentCreate`, `StudentUpdate`) para representação e validação de corpo.
- `app/services/studentService.py`: Classe encarregada pela inteligência e persistência (em memória) do negócio de alunos.
- `test/test_api.py`: Setup das suítes de teste de integração.
- `Dockerfile` e `docker-compose.yaml`: Configuração via Docker para empacotar a aplicação e o contexto de testes de maneira reproduzível.

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

- `POST /api/v1/alunos/`: Cria um novo aluno 
- `GET /api/v1/alunos/{student_id}`: Recupera informações detalhadas a partir do id do aluno
- `GET /api/v1/alunos/`: Lista todos os alunos já criados
- `PATCH /api/v1/alunos/{student_id}`: Modifica parcialmente os dados informados de um aluno específico
- `DELETE /api/v1/alunos/{student_id}`: Remove permanentemente um aluno
- `DELETE /api/v1/alunos/`: Função de controle que reseta e remove todos os alunos do sistema
