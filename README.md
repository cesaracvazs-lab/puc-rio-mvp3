# Sistema de Controle de Pacientes

API principal para o gerenciamento de pacientes com cadastro, busca, filtros avançados, paginação, ordenação dinâmica e integração com ViaCEP e com a API secundária de alertas para calcular o retorno do paciente.

## Objetivo

O sistema ajuda clínicas, consultórios e unidades de atendimento a organizar e consultar pacientes de forma prática, com regras de busca e filtros por nome, e-mail e endereço, além de manter histórico de visitas e situação clínica.

## Arquitetura

A aplicação segue o cenário 2 do MVP: a API principal consulta o ViaCEP para obter dados do endereço, persiste os pacientes no SQLite e chama a API secundária de Alertas e Calendário de Retorno quando existe `ultima_visita`.

![Arquitetura do MVP](docs/arquitetura_mvp.svg)

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Requests

### Comunicação com a API secundária

Por padrão, a API principal procura a API de alertas em:

```text
http://127.0.0.1:8001
```

Esse endereço pode ser alterado pela variável `ALERTA_RETORNO_URL`.

## API externa utilizada

- ViaCEP
- URL base: https://viacep.com.br/ws/{cep}/json/
- Licença: uso livre para consulta pública, conforme documentação do serviço.
- Cadastro: não exige cadastro para uso básico.
- Rota utilizada: GET para consulta de um CEP específico.

## Requisitos

- Python 3.12+
- Pip
- Docker

## Instalação local

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd controle_pacientes
   ```
2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Inicie a API:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
5. Acesse a documentação Swagger:
   - http://localhost:8000/docs
   - http://localhost:8000/redoc

## Endpoints principais

### GET /pacientes
Lista pacientes com filtros, paginação e ordenação.

Parâmetros:
- nome
- email
- endereco
- situacao
- page
- page_size
- order_by: nome ou ultima_visita
- order_direction: asc ou desc

### POST /pacientes
Cria um novo paciente com preenchimento automático do endereço via ViaCEP e calcula o alerta de retorno quando `ultima_visita` é informada.

### GET /pacientes/{paciente_id}
Busca um paciente por ID.

### PUT /pacientes/{paciente_id}
Atualiza os dados do paciente e recalcula o alerta quando `ultima_visita` ou `situacao` é alterada.

### DELETE /pacientes/{paciente_id}
Remove um paciente.

## Persistência

O banco de dados SQLite é armazenado no arquivo:

```bash
pacientes.db
```

## Executando com Docker

Crie uma rede para permitir a comunicação entre os dois containers:

```bash
docker network create mvp-rede
```

1. Construa a imagem da API secundária no repositório `alerta_retorno`:
   ```bash
   docker build -t api-alerta-retorno .
   ```
2. Inicie a API secundária na rede do MVP:
   ```bash
   docker run --rm --name alerta-retorno \
     --network mvp-rede \
     -p 8001:8001 \
     api-alerta-retorno
   ```
3. Construa a imagem da API principal:
   ```bash
   docker build -t controle-pacientes .
   ```
4. Execute a API principal na rede do MVP:
   ```bash
   docker run --rm --name controle-pacientes \
     --network mvp-rede \
     -e ALERTA_RETORNO_URL=http://alerta-retorno:8001 \
     -p 8000:8000 \
     controle-pacientes
   ```

   O SQLite fica disponível durante a execução do container. Para preservar o
   banco entre execuções, configure posteriormente um volume para o caminho
   específico do arquivo `pacientes.db`, sem montar o volume sobre `/app`.

5. Acesse a documentação:
   - http://localhost:8000/docs

A API secundária deve estar executando na mesma rede. Consulte o README do
repositório `alerta_retorno` para construir e iniciar o container `alerta-retorno`.

## Observações

- O nome dos arquivos e variáveis segue a convenção snake_case.
- As classes e schemas Pydantic seguem a convenção CamelCase.
- A API principal foi projetada para atender ao requisito mínimo de CRUD e também oferecer filtros, paginação e ordenação dinâmica.
