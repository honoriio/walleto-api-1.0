# Área exclusiva para importações
import re 
import datetime

def nome_usuario(): # ---> refatorar e tirar o try o mesmo não tem necessidade de estar aqui.
    while True:
        nome = input('Nome do usuário: ').strip()
            
        if not nome: # --> VALIDAÇÃO 1, VERIFICA SE A STRING ESTA VAZIA
            print("O nome não pode estar vazio.")
            continue
            
        if len(nome) >= 100: #-->  VALIDAÇÃO 2, O NOME NÃO PODE TER MAIS DE 100 CARACTERES
            print("O nome não pode ter mais que 100 caracteres.")
            continue

        return nome
            



def email_usuario():
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' # --> PADRÃO DE CARACTERES QUE É USADO NOS EMAILS.
    while True:
        email = input("Digite o e-mail: ")

        if not email: # --> VERIFICA SE A VARIAVEK EMAIL ESTA VAZIA
            print("O e-mail não pode estar em branco.")
            
        if re.match(padrao, email): # --> FAZ A VERIFICAÇÃO SE O EMAIL SEGUE O PADRÃO CORRETO
            print("E-mail válido!")
            return email
        else:
            print('O e-mail informado não é válido.')
        

def sexo_usuario():
    masculino = "Masculino"
    feminino = "Feminino"
    while True:
        try:
            print("-" * 60)
            print("[1] - MASCULINO")
            print("[2] - FEMININO")
            print("-" * 60)
            escolha = int(input("opção: "))

            if escolha == 1:
                sexo = masculino
                return sexo 
            elif escolha == 2:
                sexo = feminino
                return sexo
            else:
                raise ValueError("Opção invalida.")
            
        except ValueError as erro:
            print(f"ERRO: {erro}")


def data_nascimento_usuario():  # --> foi criado por inteligencia artificial. sou pessimo com datas,por isso eu pedi ajuda com essa função.
    data_atual = datetime.date.today()

    while True:
        data_nasc_str = input("Informe a data de nascimento (DD/MM/AAAA): ").strip()

        # Validação 1: Trata entrada vazia (diferente do data_gasto, aqui é um erro)
        if not data_nasc_str:
            print("ERRO: A data de nascimento é obrigatória. Tente novamente.")
            continue # Volta para o início do loop

        # Validação 2: Permite que o usuário digite DDMMAAAA sem separadores
        if len(data_nasc_str) == 8 and data_nasc_str.isdigit():
            data_nasc_str = f"{data_nasc_str[0:2]}/{data_nasc_str[2:4]}/{data_nasc_str[4:8]}"

        # Validação 3: Permite outros separadores comuns ('.', '-', etc.)
        data_limpa = data_nasc_str.replace('.', '/').replace('-', '/').replace('_', '/')

        try:
            # Tenta converter a string limpa para um objeto de data
            data_nasc_obj = datetime.datetime.strptime(data_limpa, "%d/%m/%Y").date()

            # --- VALIDAÇÕES LÓGICAS PARA DATA DE NASCIMENTO ---

            # Validação 4: A data de nascimento não pode ser no futuro
            if data_nasc_obj > data_atual:
                print(f"ERRO: A data {data_nasc_obj.strftime('%d/%m/%Y')} é no futuro. Impossível!")
                continue # Volta para o início do loop

            # Se todas as validações passaram, podemos calcular a idade
            idade = data_atual.year - data_nasc_obj.year
            
            # Ajuste fino para quem ainda não fez aniversário no ano corrente
            if (data_atual.month, data_atual.day) < (data_nasc_obj.month, data_nasc_obj.day):
                idade -= 1

            # Validação 5: Checa se a idade é razoável (evita erros como 1825 em vez de 1925)
            if idade > 120:
                print(f"ERRO: A idade calculada ({idade} anos) é muito alta. Verifique o ano digitado.")
                continue # Volta para o início do loop

            # Se chegamos até aqui, a idade é válida!
            print(f"Você tem {idade} anos.")
            break # Quebra o loop 'while' e encerra a função

        except ValueError:
            # Erro pego pelo strptime (ex: 30/02/2023, ou texto aleatório)
            print("ERRO: Formato de data inválido ou data não existe. Por favor, use DD/MM/AAAA.")
            # O 'continue' aqui é implícito, o loop vai rodar novamente
