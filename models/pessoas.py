from db import conectar

def cadastrar_pessoa(nome, idade, peso):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO pessoas (nome, idade, peso) VALUES (%s, %s, %s)",
                   (nome, idade, peso))
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_pessoas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pessoas")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def deletar_pessoa(id_pessoa):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM pessoas WHERE id = %s", (id_pessoa,))
    conexao.commit()
    afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return afetadas

def calcular_medias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT AVG(idade), AVG(peso) FROM pessoas")
    medias = cursor.fetchone()
    cursor.close()
    conexao.close()
    return medias
