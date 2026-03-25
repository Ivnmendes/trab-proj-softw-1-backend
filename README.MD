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

## 3. Banco de Dados (PostgreSQL)

1. Crie um banco de dados local chamado `farmacia_db`.
2. Configure as variáveis de ambiente no arquivo `/core/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'farmacia_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
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
