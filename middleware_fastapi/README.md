# Middleware FastAPI

<p align="center">
	<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" />
	<img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
	<img src="https://img.shields.io/badge/Uvicorn-Server-2B2B2B?style=for-the-badge&logo=uvicorn&logoColor=white" />
	<img src="https://img.shields.io/badge/Pydantic-Validation-E92063?style=for-the-badge&logo=pydantic&logoColor=white" />
	<img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

API REST simples desenvolvida com FastAPI para demonstrar uma estrutura básica de projeto com:

- rotas organizadas por responsabilidade
- modelo de domínio com Pydantic
- validação de entrada e saída
- middleware HTTP para medição de tempo de resposta
- execução local e via Docker

O projeto utiliza armazenamento em memória, por isso os dados são perdidos quando a aplicação reinicia.

## Visão Geral

Este repositório foi organizado para servir como base de estudo e como referência de uma aplicação FastAPI pequena, porém estruturada de forma escalável.

O fluxo principal é:

1. A aplicação recebe a requisição em `main.py`.
2. O middleware registra o tempo de processamento e adiciona o header `X-Process-Time` na resposta.
3. As rotas de usuário processam as operações de CRUD em uma lista em memória.
4. Os dados são validados com modelos Pydantic.

## Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Docker

## Estrutura do Projeto

```text
middleware_fastapi/
├── app/
│   ├── Dockerfile
│   ├── models/
│   │   └── user.py
│   ├── routes/
│   │   ├── middleware.py
│   │   └── user.py
│   └── schemas/
│       └── user.py
├── main.py
├── requirements.txt
└── docker-compose.yml
```

### Responsabilidade dos arquivos

- `main.py`: ponto de entrada da aplicação FastAPI.
- `app/routes/user.py`: endpoints de criação, consulta, atualização e exclusão de usuários.
- `app/routes/middleware.py`: middleware HTTP que mede o tempo de processamento da requisição.
- `app/models/user.py`: modelo de resposta da entidade `User`.
- `app/schemas/user.py`: schema de entrada para criação e atualização de usuário.
- `app/Dockerfile`: imagem da aplicação.
- `docker-compose.yml`: orquestração do serviço com Docker Compose.

## Middleware

O projeto registra um middleware HTTP global com a função `add_process_time_header`.

### Comportamento

- intercepta cada requisição HTTP
- mede o tempo de processamento com `time.perf_counter()`
- adiciona o header `X-Process-Time` na resposta
- escreve uma linha de log no terminal com o método, a URL e o tempo gasto

### Exemplo de header retornado

```http
X-Process-Time: 0.003421
```

## Endpoints

### Health check

`GET /`

Retorna o status básico da aplicação.

#### Resposta

```json
{
	"status": "ok"
}
```

### Criar usuário

`POST /users/`

Cria um novo usuário em memória.

#### Payload

```json
{
	"name": "Maria Silva",
	"email": "maria@example.com"
}
```

#### Respostas

- `201 Created`: usuário criado com sucesso
- `400 Bad Request`: email já existente

#### Exemplo de resposta

```json
{
	"id": 1,
	"name": "Maria Silva",
	"email": "maria@example.com"
}
```

### Listar usuários

`GET /users/`

Retorna todos os usuários cadastrados em memória.

#### Exemplo de resposta

```json
[
	{
		"id": 1,
		"name": "Maria Silva",
		"email": "maria@example.com"
	}
]
```

### Buscar usuário por ID

`GET /users/{user_id}`

#### Respostas

- `200 OK`: usuário encontrado
- `404 Not Found`: usuário não encontrado

### Atualizar usuário

`PUT /users/{user_id}`

Atualiza nome e email de um usuário existente.

#### Payload

```json
{
	"name": "Maria Souza",
	"email": "maria.souza@example.com"
}
```

#### Respostas

- `200 OK`: usuário atualizado
- `400 Bad Request`: email já existente em outro usuário
- `404 Not Found`: usuário não encontrado

### Remover usuário

`DELETE /users/{user_id}`

Remove um usuário da lista em memória.

#### Resposta

- `204 No Content`

## Modelos de Dados

### UserCreate

Schema de entrada usado no `POST` e `PUT`.

```json
{
	"name": "string",
	"email": "string"
}
```

### User

Modelo de saída com identificador interno.

```json
{
	"id": 1,
	"name": "string",
	"email": "string"
}
```

## Execução Local

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Subir a aplicação

```bash
uvicorn main:app --reload
```

### 3. Acessar a API

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## Execução com Docker

### Build e subida do serviço

```bash
docker compose up --build
```

### Acessar a API

- http://127.0.0.1:8000

## Exemplos de Consumo

### Criar usuário com curl

```bash
curl -X POST http://127.0.0.1:8000/users/ \
	-H "Content-Type: application/json" \
	-d '{"name":"Maria Silva","email":"maria@example.com"}'
```

### Listar usuários com curl

```bash
curl http://127.0.0.1:8000/users/
```

### Buscar usuário por ID com curl

```bash
curl http://127.0.0.1:8000/users/1
```

## Limitações Atuais

- o banco de dados é simulado com uma lista em memória
- os dados não persistem após reiniciar a aplicação
- não há autenticação, autorização ou camadas de serviço/repositório
- o projeto é propositalmente simples para fins educacionais

## Melhorias Futuras

- substituir o armazenamento em memória por banco relacional
- adicionar camada de serviços e repositórios
- incluir testes automatizados
- adicionar autenticação com JWT
- padronizar logs estruturados

## Observações de Implementação

- O pacote `email-validator` é necessário para validação de `EmailStr` no Pydantic.
- O middleware adiciona o header `X-Process-Time` e também escreve logs no console.
- A aplicação deve ser executada com host `0.0.0.0` dentro do container para ficar acessível externamente.

## Licença

Projeto acadêmico.
