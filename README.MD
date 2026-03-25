# Projeto Software 1 - Backend

## 1. Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- **Python 3.10+**
- **Poetry** (Gerenciador de dependências)
- **PostgreSQL 18+**

## 2. Configuração do Ambiente

### Instalar Dependências

O Poetry criará um ambiente virtual isolado e instalará todas as bibliotecas registradas no `poetry.lock`.

```bash
poetry install
```

### Ativar o Ambiente Virtual

Sempre execute este comando antes de rodar qualquer script do Django:

```bash
poetry shell
```

## 3. Variáveis de ambiente

1. Crie um arquivo `.env` com base em `.env.example`.
2. Configure as variáveis de ambiente no arquivo:

```env
SECRET_KEY=# chave aleatória, pode ser gerada com: "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
DEBUG=# Use "True" quando em dev e "False" na produção
ALLOWED_HOSTS=# "localhost,127.0.0.1" quando local ou o ip do render
# Seu usuario e senha postgres
DATABASE_URL=postgres://<user>:<senha>@localhost:5432/farmacia_db
```

### Rodar Migrations

Prepare a estrutura das tabelas (Medicamentos, CIDs, Documentos, etc):

```bash
python manage.py migrate
```

## 4. Executando o Servidor

Para iniciar o serviço de desenvolvimento:

```bash
python manage.py runserver
```

O projeto estará disponível em `http://127.0.0.1:8000`.

## 5. Comandos Úteis do Poetry

- **Adicionar nova biblioteca:** `poetry add <pacote>`
- **Adicionar dependência de dev:** `poetry add <pacote> --group dev`
- **Atualizar dependências:** `poetry update`
- **Verificar ambiente ativo:** `poetry env info`
