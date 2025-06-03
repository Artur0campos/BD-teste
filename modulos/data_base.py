import mysql.connector
from mysql.connector import Error


def conectar_ao_banco():
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            database="filiais_BD"
        )
        if conexao.is_connected():
            print("Conexão bem-sucedida ao banco de dados!")
            return conexao

    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


conn = conectar_ao_banco()

if conn: 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assinante_tbl")
    resultado = cursor.fetchall()

    for linha in resultado:
        print(linha)

    cursor.close()
    conn.close()

def inserir_tipo(descricao):
    conn = conectar_ao_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO assinante_tbl (nome) VALUES (%s)", (descricao,))
        conn.commit()
        print("tipo inserido com sucesso")
        conn.close()
        cursor.close()

def inserir_ramo(descricao):
    conn = conectar_ao_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO assinante_tbl (nome) VALUES (%s)", (descricao,))
        conn.commit()
        print("ramo inserido com sucesso")
        conn.close()
        cursor.close()

def inserir_assinante(nome, fk_cd_tipo, fk_cd_ramo):
    try:
        conn = conectar_ao_banco()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO assinante_tbl (fk_cd_ramo, fk_cd_tipo, nome) VALUES (%s, %s, %s)", 
                         (fk_cd_ramo, fk_cd_tipo, nome))
            conn.commit()
            conn.close()
            cursor.close()
    except Exception as e:
        # Você pode personalizar a mensagem para diferentes tipos de erro
        if "foreign key constraint fails" in str(e).lower():
            raise Exception("Erro: Tipo ou Ramo inválido (ID não existe)")
        elif "duplicate entry" in str(e).lower():
            raise Exception("Erro: Já existe um assinante com esses dados")
        else:
            raise Exception(f"Erro ao inserir no banco de dados: {e}")


def listar_assinantes():
    conn = conectar_ao_banco()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM assinante_tbl")
        return print(cursor.fetchall())
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def update_assinante(cd_assinante, nome, fk_cd_tipo, fk_cd_ramo):
    conn = conectar_ao_banco()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE assinante_tbl SET nome = %s, fk_cd_tipo = %s, fk_cd_ramo = %s WHERE cd_assinante = %s",
            (nome, fk_cd_tipo, fk_cd_ramo, cd_assinante)
        )
        conn.commit()
    except Exception as e:
        raise Exception(f"Erro ao atualizar assinante: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_assinante(cd_assinante):
    conn = conectar_ao_banco()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM assinante_tbl WHERE cd_assinante = %s"
        cursor.execute(sql, (cd_assinante,))
        conn.commit()
        print("Assinante excluído com sucesso")
        cursor.close()

def obter_assinante_por_id(cd_assinante):
    conn = conectar_ao_banco()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM assinante_tbl WHERE cd_assinante = %s",
            (cd_assinante,)
        )
        return cursor.fetchone()
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def menu():
    while True:
        try:
            print("\n--- MENU CRUD ---")
            print("1 - Inserir assinante")
            print("2 - Listar assinantes")
            print("3 - Atualizar assinante")
            print("4 - Deletar assinante")
            print("0 - Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                try:
                    nome = input("Nome do assinante: ")
                    fk_cd_tipo = int(input("id do tipo: "))
                    fk_cd_ramo = int(input("id do ramo: "))
                    inserir_assinante(nome, fk_cd_tipo, fk_cd_ramo)
                    print("Assinante inserido com sucesso!")
                except Exception as e:
                    print(f"Erro ao inserir assinante: {e}")
                    continue 

            elif opcao == "2":
                try:
                    listar_assinantes()
                except Exception as e:
                    print(f"Erro ao listar assinantes: {e}")
                    continue

            elif opcao == "3":
                try:
                    id = int(input("ID do assinante a atualizar: "))
                    novo_nome = input("Novo nome: ")
                    novo_tipo = int(input("Novo ID do tipo: "))
                    novo_ramo = int(input("Novo ID do ramo: "))
                    update_assinante(id, novo_nome, novo_tipo, novo_ramo)
                except Exception as e:
                    print(f"Erro ao atualizar assinante: {e}")
                    continue

            elif opcao == "4":
                try:
                    id = int(input("ID do assinante a deletar: "))
                    delete_assinante(id)
                except Exception as e:
                    print(f"Erro ao deletar assinante: {e}")
                    continue

            elif opcao == "0":
                print("Saindo...")
                break

            else:
                print("Opção inválida.")

        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            continue



menu()
