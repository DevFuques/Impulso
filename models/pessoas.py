from db import conectar

import urllib.request
import json

def buscar_endereco_por_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                dados = json.loads(response.read().decode("utf-8"))
                if "erro" not in dados:
                    return {
                        "logradouro": dados.get("logradouro", ""),
                        "bairro": dados.get("bairro", ""),
                        "cidade": dados.get("localidade", ""),
                        "estado": dados.get("uf", "")
                    }
    except Exception as e:
        print("Erro ao buscar CEP:", e)
    return None

def cadastrar_pessoa(nome, idade, peso, cep, logradouro, bairro, cidade, estado):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO pessoas (nome, idade, peso, cep, logradouro, bairro, cidade, estado) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (nome, idade, peso, cep, logradouro, bairro, cidade, estado))
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_pessoas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, idade, peso, cep, logradouro, bairro, cidade, estado FROM pessoas")
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def deletar_pessoa(pessoa_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM pessoas WHERE id = %s", (pessoa_id,))
    conexao.commit()
    cursor.close()
    conexao.close()

def calcular_medias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT AVG(idade), AVG(peso) FROM pessoas")
    medias = cursor.fetchone()
    cursor.close()
    conexao.close()
    return medias
