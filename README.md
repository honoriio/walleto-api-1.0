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
├── src/
│   ├── core/             # Configurações centrais do projeto
│   ├── domain/           # Entidades e regras de negócio
│   ├── application/      # Casos de uso da aplicação
│   ├── infrastructure/   # Persistência, banco de dados e integrações
│   └── api/              # Rotas e camada HTTP
├── tests/                # Testes automatizados
├── requirements.txt
├── README.md
└── main.py
