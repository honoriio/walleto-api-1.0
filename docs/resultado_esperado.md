

# 🚀 Plano de execução por commits (Walleto)

## 🔹 Commit 1 — Mover Dashboard

**Mensagem do commit:**

```
refactor: move dashboard para camada de infrastructure
```

**Ações:**

* [ ] Criar pasta: `src/infrastructure/dashboard/`
* [ ] Mover:

  * `src/services/dashboard.py`
    → `src/infrastructure/dashboard/streamlit_dashboard.py`
* [ ] Atualizar imports no projeto inteiro

**Por quê:**
Separar interface técnica (Streamlit) da regra de negócio.

---

## 🔹 Commit 2 — Mover Exportador Excel

**Mensagem do commit:**

```
refactor: move exportador excel para infrastructure/exporters
```

**Ações:**

* [ ] Criar pasta: `src/infrastructure/exporters/`
* [ ] Mover:

  * `src/services/exportador_excel.py`
    → `src/infrastructure/exporters/excel_exporter.py`
* [ ] Atualizar imports

**Por quê:**
Exportação é infraestrutura, não regra de negócio.

---

## 🔹 Commit 3 — Criar Controllers

**Mensagem do commit:**

```
feat: cria camada de controllers para orquestração da aplicação
```

**Ações:**

* [ ] Criar pasta: `src/controllers/`
* [ ] Criar arquivo: `gasto_controller.py`

**Adicionar funções (mesmo que simples no começo):**

* [ ] `adicionar_gasto_controller`
* [ ] `editar_gasto_controller`
* [ ] `excluir_gasto_controller`
* [ ] `listar_gastos_controller`
* [ ] `filtrar_gastos_controller`
* [ ] `exportar_gastos_controller`
* [ ] `abrir_dashboard_controller`

**Por quê:**
Centralizar fluxo e parar de misturar view com regra.

---

## 🔹 Commit 4 — Desacoplar Views do Repository

**Mensagem do commit:**

```
refactor: remove acesso direto ao repository das views e conecta via controller
```

**Ações:**

* [ ] Remover imports de repository dentro de:

  * `gastos_views.py`
  * `menus.py`
* [ ] Fazer views chamarem controllers
* [ ] Controllers passam a chamar repository/service

**Por quê:**
View NÃO deve acessar banco diretamente.

---

## 🔹 Commit 5 — Limpar Repository

**Mensagem do commit:**

```
refactor: limpa repository mantendo apenas acesso a dados
```

**Ações:**

**Remover do repository:**

* [ ] `print(...)`
* [ ] formatação de moeda/data
* [ ] exibição de dados
* [ ] `calcular_gastos(...)`

**Manter:**

* [ ] CRUD (inserir, buscar, editar, excluir)
* [ ] consultas puras

**Por quê:**
Repository = banco de dados apenas.

---

## 🔹 Commit 6 — Criar Utils e extrair validações

**Mensagem do commit:**

```
refactor: extrai validações e manipulação de dados para utils
```

**Ações:**

* [ ] Criar:

  * `src/utils/validators.py`
  * `src/utils/datas.py`
  * `src/utils/formatters.py`

**Mover de `gastos_views.py`:**

* [ ] validação de nome
* [ ] validação de valor
* [ ] validação de categoria
* [ ] validação de descrição
* [ ] validação/conversão de data

**Por quê:**
Reutilização + organização + código limpo.

---

## 🔹 Commit 7 — Criar Relatorio View

**Mensagem do commit:**

```
feat: cria relatorio_view para exibição de dados e resultados
```

**Ações:**

* [ ] Criar: `src/views/relatorio_view.py`
* [ ] Mover para lá:

  * prints de resultados
  * exibição de filtros
  * listagem formatada
  * totais

**Por quê:**
Separar entrada (input) de saída (output).

---

## 🔹 Commit 8 — Ajustar menus.py

**Mensagem do commit:**

```
refactor: simplifica menus mantendo apenas interação com usuário
```

**Ações:**

* [ ] Remover validações de negócio
* [ ] Remover lógica de verificação de ID no banco
* [ ] Deixar apenas:

  * exibição de menu
  * leitura de input

**Por quê:**
Menu = interface pura.

---

## 🔹 Commit 9 — Revisão final da arquitetura

**Mensagem do commit:**

```
chore: organiza estrutura final do projeto conforme arquitetura definida
```

**Ações:**

* [ ] Revisar imports
* [ ] Garantir que fluxo está assim:

```
View → Controller → Service → Repository
```

* [ ] Garantir que:

  * `services` = regra de negócio
  * `repositories` = banco
  * `views` = interface
  * `controllers` = orquestração
  * `infrastructure` = externo (excel, dashboard)