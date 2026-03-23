from src.core.database import get_connection
from decimal import Decimal
from src.core.constants import*
from src.models.gastos import Gasto


def inserir_gasto_repository(gasto): # insere os valores informados pelo usuario a tabela gastos 
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gastos (nome, valor, categoria, descricao, data) VALUES (?, ?, ?, ?, ?)", 
                (gasto.nome, str(gasto.valor), gasto.categoria, gasto.descricao, gasto.data)
            )
            if cursor.rowcount > 0:
                conn.commit()
                return {"status": "sucesso", "mensagem": "Gasto Cadastrado com Sucesso!"}
            else:
                return {"status": "erro", "mensagem": "Nenhum gasto cadastrado"}
            
    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro ao cadastrar gasto: {e}"}



def excluir_gastos_repository(id): # exclui o gasto com base no ID informado pelo usuario
     try: 
         with get_connection() as conn: 
             cursor = conn.cursor()
             cursor.execute("SELECT * FROM gastos WHERE id = ?", (id,))
             if cursor.fetchone() is None: 
                 return {"status": "erro", "mensagem": "Nenhum gasto encontrado com esse ID."}
             cursor.execute("DELETE FROM gastos WHERE id = ?", (id,))
             if cursor.rowcount > 0: 
                 conn.commit() 
                 return {"status": "sucesso", "mensagem": f"Gasto com ID {id} foi excluído com sucesso."} 
             else: 
                 return {"status": "erro", "mensagem": "Falha ao excluir o gasto."}
     except Exception as e: 
         return {"status": "erro", "mensagem": f"Erro ao excluir o gasto: {str(e)}"}




def buscar_gasto_por_id_repository(id: int):
    """Busca um gasto no banco e retorna um objeto Gasto ou None."""
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos WHERE id = ?", (id,))
        resultado = cursor.fetchone()

        if not resultado:
            return None

        return Gasto(
            id=resultado[0],
            nome=resultado[1],
            valor=resultado[2],
            categoria=resultado[3],
            descricao=resultado[4],
            data=resultado[5],
        )



def editar_gastos_repository(dados): 
   
    try:  
         # Validação inicial do ID. O ID não pode estar vazio.
         id_gasto = dados.get("id")
         if not id_gasto:
             return {"status": "erro", "mensagem": "ID do gasto não fornecido."}

         with get_connection() as conn: 
            cursor = conn.cursor() 

            # --- Passo 1: Buscar dados antigos ---
            cursor.execute("SELECT nome, valor, categoria, descricao, data FROM gastos WHERE id = ?", (id_gasto,)) 
            resultado = cursor.fetchone() 

            if not resultado: 
                return {"status": "erro", "mensagem": "Gasto não encontrado."} 

            nome_antigo, valor_antigo, categoria_antiga, descricao_antiga, data_antiga = resultado 


            # Se o novo valor (dados.get(campo)) existir E não for uma string vazia, use-o.
            # Caso contrário (se for None ou ""), mantenha o valor antigo.
            
            nome_novo = dados.get("nome")
            nome = nome_novo if nome_novo else nome_antigo
            
            categoria_nova = dados.get("categoria")
            categoria = categoria_nova if categoria_nova else categoria_antiga
            
            descricao_nova = dados.get("descricao")
            descricao = descricao_nova if descricao_nova else descricao_antiga
            
            data_nova = dados.get("data")
            data = data_nova if data_nova else data_antiga


    
            valor = valor_antigo # Assume o valor antigo por padrão
            valor_novo_str = dados.get("valor")
            
            if valor_novo_str: # Apenas tenta atualizar se um novo valor foi fornecido
                try:
                    valor = float(valor_novo_str)
                except (ValueError, TypeError):
                    # Se a conversão falhar (ex: "abc" ou um formato inválido), 
                    # o código ignora a alteração e mantém o valor_antigo.
                    pass 

            cursor.execute(""" 
                UPDATE gastos 
                SET nome = ?, valor = ?, categoria = ?, descricao = ?, data = ? 
                WHERE id = ? 
            """, (nome, valor, categoria, descricao, data, id_gasto)) 

            if cursor.rowcount > 0: 
                conn.commit() 
                return {"status": "sucesso", "mensagem": "Gasto editado com sucesso!"} 
            else: 
                # Isso pode acontecer se os dados novos forem idênticos aos antigos.
                return {"status": "info", "mensagem": "Nenhuma alteração detectada, os dados já estavam atualizados."}
            
    except KeyError as e: 
         return {"status": "erro", "mensagem": f"Chave {e} não encontrada nos dados fornecidos."} 
    except Exception as e: 
         # Captura genérica para outros erros inesperados (ex: falha de conexão)
         return {"status": "erro", "mensagem": f"Erro inesperado ao editar gasto: {e}"}




def listar_gastos_repository():
    """Busca todos os gastos e retorna uma lista de objetos Gasto."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos")
        resultados = cursor.fetchall()
        
        gastos_objetos = []
        for tupla in resultados:
            gastos_objetos.append(
                Gasto(
                    id=tupla[0],
                    nome=tupla[1],
                    valor=tupla[2],
                    categoria=tupla[3],
                    descricao=tupla[4],
                    data=tupla[5]
                )
            )

        return gastos_objetos



def converter_data_para_banco(data_str: str) -> str:
    return data_str.strftime("%Y-%m-%d")


def filtrar_gastos_data_repository(data_inicio, data_final):
    data_inicio = converter_data_para_banco(data_inicio)
    data_final = converter_data_para_banco(data_final)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM gastos WHERE data BETWEEN ? AND ?",
            (data_inicio, data_final)
        )
        resultados = cursor.fetchall()

        gastos_objetos = []
        for tupla in resultados:
            gastos_objetos.append(
                Gasto(
                    id=tupla[0],
                    nome=tupla[1],
                    valor=Decimal(str(tupla[2])),
                    categoria=tupla[3],
                    descricao=tupla[4],
                    data=tupla[5]
                )
            )

        return gastos_objetos


def filtrar_gasto_valor_repository(valor_min, valor_max):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM gastos WHERE valor BETWEEN ? AND ?",
            (str(valor_min), str(valor_max))
        )
        resultados = cursor.fetchall()

        gastos_objetos = []
        for tupla in resultados:
            gastos_objetos.append(
                Gasto(
                    id=tupla[0],
                    nome=tupla[1],
                    valor=tupla[2],
                    categoria=tupla[3],
                    descricao=tupla[4],
                    data=tupla[5],
                )
            )

        return gastos_objetos



def filtrar_gastos_categoria_repository(categoria):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gastos WHERE categoria = ?", (categoria,))
            resultados = cursor.fetchall()

            return [
                Gasto(
                    id=tupla[0],
                    nome=tupla[1],
                    valor=tupla[2],
                    categoria=tupla[3],
                    descricao=tupla[4],
                    data=tupla[5],
                )
                for tupla in resultados
            ]

    except Exception:
        return None


def filtrar_gastos_nome_repository(nome):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos WHERE nome = ?", (nome,))
        resultados = cursor.fetchall()

        return [
            Gasto(
                id=tupla[0],
                nome=tupla[1],
                valor=tupla[2],
                categoria=tupla[3],
                descricao=tupla[4],
                data=tupla[5],
            )
            for tupla in resultados
        ]

