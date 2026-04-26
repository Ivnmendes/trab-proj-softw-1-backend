# Documentação dos Endpoints de Medicamentos

Este documento descreve como consumir os endpoints do módulo de medicamentos.

## Base URL

Em ambiente local (Django padrão):

`http://localhost:8000`

Rotas deste módulo ficam sob:

`http://localhost:8000/medications/`

## Autenticação

No estado atual, os endpoints de API de medicamentos estão públicos (sem autenticação obrigatória), pois as views usam AllowAny.

## Endpoints Disponíveis

## 1. Listar medicamentos

Método: GET  
URL: /medications/api/

Descrição:
Retorna uma lista de medicamentos no formato público definido em MedicationPublicSerializer.

Exemplo com curl:

`curl -X GET "http://localhost:8000/medications/api/"`

Resposta de exemplo:

{
  "id": 3,
  "nome": "Amoxicilina 500mg",
  "principioAtivo": "Amoxicilina",
  "apresentacao": "500mg",
  "disponivel": false,
  "unidadeSaude": "Sem estoque no momento",
  "descricao": "Antibiótico utilizado no tratamento de diversas infecções bacterianas.",
  "tipo": "BASIC",
  "farmacias": [],
  "cids": [],
  "documentos": [],
  "created_at": "2026-04-26T12:00:00Z",
  "updated_at": "2026-04-26T12:00:00Z"
}

## 2. Buscar medicamento por id

Método: GET  
URL: `/medications/api/{id}/`

Descrição:
Retorna os detalhes de um medicamento específico.

Exemplo com curl:

`curl -X GET "http://localhost:8000/medications/api/3/"`

Respostas esperadas:

- 200 OK: medicamento encontrado.
- 404 Not Found: medicamento não encontrado.

## Campos retornados pela API pública

- id: identificador do medicamento.
- nome: nome exibível montado com base em name e concentration.
- principioAtivo: campo generic_name.
- apresentacao: campo concentration.
- disponivel: true quando existe pelo menos uma farmácia vinculada.
- unidadeSaude:
  - Sem estoque no momento, quando não há farmácia vinculada.
  - Nome da farmácia, quando há apenas uma.
  - Lista de nomes, quando há múltiplas farmácias.
- descricao: campo description.
- tipo: tipo do medicamento (BASIC, SPECIALIZED, POPULAR).
- farmacias: lista de farmácias vinculadas.
- cids: lista de CIDs vinculados (incluindo documentos do CID).
- documentos: lista de documentos vinculados diretamente ao medicamento.
- created_at: data de criação.
- updated_at: data de atualização.

## Estrutura de farmacias

Cada item de farmacias inclui:

- id
- name
- description
- type
- address
- latitude
- longitude
- phone
- created_at
- updated_at

## Endpoint administrativo já existente

Além da API, existe um endpoint administrativo para importação de medicamentos:

Método: GET e POST  
URL: /medications/admin/import-medications/

Esse endpoint é protegido para staff e renderiza formulário HTML de importação.

## Teste rápido

1. Inicie o servidor:
python manage.py runserver

2. Acesse a lista:
`http://localhost:8000/medications/api/`

3. Acesse um detalhe:
http://localhost:8000/medications/api/1/
