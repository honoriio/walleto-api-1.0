
# Organização do Projeto Walleto

## Objetivo

Separar responsabilidades para:

- evitar bagunça
- facilitar manutenção
- reduzir erros
- preparar o projeto para crescer no futuro, como API ou versão web

---

## Regra principal

Cada parte do sistema deve ter uma responsabilidade clara.

Em resumo:

- quem cuida da interface não cuida da regra de negócio
- quem cuida da regra de negócio não cuida da persistência
- quem cuida dos dados não deve falar com o usuário

---

## Estrutura base


walleto/
│
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── .gitignore
│
├── data/
│   └── walleto.db
│
├── docs/
│   ├── arquitetura.md
│   ├── regras-negocio.md
│   └── fluxos.md
│
├── logs/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
└── src/
    ├── __init__.py
    │
    ├── core/
    │   ├── config.py
    │   ├── constants.py
    │   ├── exceptions.py
    │   └── database.py
    │
    ├── domain/
    │   ├── __init__.py
    │   ├── entities/
    │   │   └── gasto.py
    │   ├── value_objects/
    │   │   └── dinheiro.py
    │   └── interfaces/
    │       └── gasto_repository.py
    │
    ├── application/
    │   ├── __init__.py
    │   ├── dto/
    │   │   ├── gasto_input.py
    │   │   └── gasto_output.py
    │   └── use_cases/
    │       ├── criar_gasto.py
    │       ├── listar_gastos.py
    │       ├── editar_gasto.py
    │       ├── remover_gasto.py
    │       ├── filtrar_gastos.py
    │       ├── gerar_relatorio.py
    │       └── exportar_gastos.py
    │
    ├── infrastructure/
    │   ├── __init__.py
    │   ├── repositories/
    │   │   └── sqlite_gasto_repository.py
    │   ├── exporters/
    │   │   └── excel_exporter.py
    │   └── dashboard/
    │       └── streamlit_dashboard.py
    │
    ├── presentation/
    │   ├── __init__.py
    │   ├── cli/
    │   │   ├── menu.py
    │   │   ├── controllers/
    │   │   │   └── gasto_controller.py
    │   │   ├── views/
    │   │   │   ├── gasto_view.py
    │   │   │   ├── relatorio_view.py
    │   │   │   └── dashboard_view.py
    │   │   └── formatters/
    │   │       └── moeda.py
    │   └── api/
    │       └── ...
    │
    └── shared/
        ├── __init__.py
        ├── validators.py
        ├── formatters.py
        └── helpers.py

---

## Responsabilidade de cada parte

### main.py

Responsável por iniciar o sistema.

Deve ter:

- função `main()`
- ponto de entrada da aplicação
- chamada do menu principal ou fluxo inicial

Não deve ter:

- regra de negócio
- leitura e gravação de dados
- funções grandes demais
- validações importantes do sistema

---

### views/

Responsável pela interação com o usuário.

Deve ter:

- `input()`
- `print()`
- menus
- mensagens exibidas ao usuário
- coleta de dados digitados

Não deve ter:

- salvar dados
- validar regra de negócio complexa
- manipular JSON, banco ou arquivos diretamente

---

### services/

Responsável pela regra de negócio.

Deve ter:

- validações
- cálculos
- regras do sistema
- processamento dos dados
- decisões do fluxo interno

Não deve ter:

- `input()`
- `print()`
- menus
- dependência direta da interface

---

### repositories/

Responsável pela persistência dos dados.

Deve ter:

- leitura de JSON, banco ou arquivos
- escrita de dados
- busca por id
- atualização e remoção de registros

Não deve ter:

- regra de negócio
- `input()`
- `print()`
- lógica de interface

---

### models/

Responsável por representar as entidades do sistema.

Deve ter:

- classes
- `dataclass`
- estrutura dos dados

Exemplo:

- `Gasto`

Não deve ter:

- interação com usuário
- persistência
- lógica pesada misturada

---

### utils/

Responsável por funções auxiliares e genéricas.

Deve ter:

- formatação
- helpers reutilizáveis
- funções pequenas de apoio

Não deve ter:

- regra de negócio principal
- funções enormes
- qualquer coisa jogada sem critério

Regra importante:

utils não é pasta de bagunça.

---

### config/

Responsável por configurações do sistema.

Deve ter:

- constantes
- caminhos de arquivos
- configurações gerais
- valores padrão do sistema

Não deve ter:

- regra de negócio
- `input()`
- lógica de fluxo

---

### data/

Responsável pelos arquivos de dados do projeto.

Deve ter:

- JSON
- arquivos exportados
- dados persistidos

Não deve ter:

- código Python
- testes
- regras do sistema

---

### logs/

Responsável pelos registros de execução.

Deve ter:

- arquivos `.log`

Não deve ter:

- código
- dados principais do sistema

---

### tests/

Responsável pelos testes do projeto.

Deve ter:

- testes unitários
- testes por camada
- cenários de validação

Não deve ter:

- código de produção
- lógica principal do sistema

---

## Fluxo correto do sistema

O fluxo ideal deve seguir esta ordem:

1. View coleta os dados do usuário  
2. Service valida e processa  
3. Repository salva ou busca os dados  
4. View exibe o resultado  

Resumo:

view -> service -> repository -> view

---

## Erros comuns que devem ser evitados

### Misturar tudo no mesmo lugar

Errado:

- receber input
- validar
- salvar
- exibir resultado

Tudo dentro da mesma função

---

### Colocar input() e print() dentro de service

Service deve cuidar da regra, não da interface.

---

### Colocar regra de negócio dentro de repository

Repository deve cuidar dos dados, não tomar decisões do sistema.

---

### Jogar tudo em utils

Quando tudo vai para utils, a organização falhou.

---

### Deixar o main.py gigante

Se o main.py está crescendo demais, é sinal de responsabilidade mal distribuída.

---

## Como decidir onde uma função deve ficar

Pergunte:

- Fala com o usuário?  
  → views  

- Aplica regra do sistema?  
  → services  

- Lê ou salva dados?  
  → repositories  

- Representa uma entidade?  
  → models  

- É auxiliar e genérica?  
  → utils  

- É configuração ou constante?  
  → config  

---

## Sinais de problema na organização

- função com input() fora de views  
- função salvando JSON fora de repositories  
- função validando regra dentro de views  
- arquivos muito grandes  
- pasta utils cheia de coisas sem relação  
- main.py concentrando lógica demais  

---

## Passo a passo para organizar

1. Listar os arquivos atuais  
2. Analisar cada função  
3. Identificar se ela pertence a interface, regra, dados, estrutura, apoio ou configuração  
4. Mover aos poucos  
5. Testar após cada mudança  

---

## Resumo final

views → entrada/saída  
services → regras  
repositories → dados  
models → estrutura  
utils → apoio  
config → configuração  

---

## Regra de ouro

Se uma pasta está fazendo o trabalho da outra, a organização está errada.