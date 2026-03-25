# Walleto API 1.0

API REST desenvolvida a partir do projeto original **Walleto**, com foco no gerenciamento de gastos pessoais de forma estruturada, organizada e escalável.

---

## Sobre o projeto

O **Walleto API 1.0** é a evolução do projeto original **Walleto 2.0**, uma aplicação de finanças pessoais desenvolvida em Python com armazenamento em SQLite.

A base original já conta com uma estrutura organizada, lógica funcional bem definida e recursos importantes para o gerenciamento financeiro, como cadastro, edição, remoção, consulta e validação de gastos.  
Nesta nova etapa, a proposta é transformar essa base em uma **API**, preservando as regras de negócio já construídas e adaptando a arquitetura para um modelo mais escalável, reutilizável e preparado para integrações futuras.

---

## Objetivo

O objetivo do projeto é transformar o Walleto em um backend capaz de:

- centralizar as regras de negócio do sistema
- disponibilizar operações por meio de endpoints
- facilitar integração com interfaces web, aplicativos e dashboards
- melhorar escalabilidade e manutenção do projeto
- servir como base para futuras evoluções do ecossistema Walleto

---

## Origem do projeto

O **Walleto API 1.0** nasce a partir do código do **Walleto original**, que já possui:

- registro de gastos com nome, valor, categoria, data e descrição
- visualização de gastos por período e categoria
- edição e remoção de registros
- validações robustas de entrada
- armazenamento local em SQLite
- organização por camadas
- base para testes automatizados

A ideia não é recomeçar do zero, mas sim **evoluir uma base já redonda**, aproveitando a lógica existente e reorganizando o sistema para o contexto de API.

---

## Funcionalidades previstas

- cadastro de gastos
- edição de gastos
- remoção de registros
- listagem de gastos
- busca por filtros
- organização por categorias
- validação de dados de entrada e saída
- base para relatórios e análises futuras

---

## Estrutura proposta

```bash
walleto-api-1.0/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── data/
│   └── walleto.db
├── docs/
│   └── organizacao_projeto.md
├── tests/
│   ├── test_gasto_service.py
│   ├── test_gasto_validators.py
│   ├── test_gasto_repository.py
│   └── test_usuario_validators.py
└── src/
    ├── api/
    │   ├── main.py
    │   ├── routes/
    │   │   ├── gasto_routes.py
    │   │   ├── usuario_routes.py
    │   │   └── dashboard.py
    │   └── schemas/
    │       ├── gasto_schema.py
    │       └── usuario_schema.py
    │
    ├── core/
    │   ├── config.py
    │   └── database.py
    │
    ├── models/
    │   ├── gasto.py
    │   └── usuario.py
    │
    ├── validators/
    │   ├── gasto_validators.py
    │   └── usuario_validators.py
    │
    ├── services/
    │   ├── gasto_service.py
    │   └── usuario_service.py
    │
    ├── repositories/
    │   ├── gasto_repository.py
    │   └── usuario_repository.py
    │
    ├── infrastructure/
    │   ├── dashboard/
    │   │   └── streamlit_dashboard.py
    │   └── exporters/
    │       ├── excel_exporter.py
    │       └── pdf_exporter.py
    │
    └── utils/
        └── formatters.py