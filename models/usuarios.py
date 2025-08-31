import hashlib
from db import conectar

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario(usuario, senha, tipo="usuario"):
    conexao = conectar()
    cursor = conexao.cursor()
    senha_hash = hash_senha(senha)
    cursor.execute("INSERT INTO usuarios (usuario, senha, tipo) VALUES (%s, %s, %s)",
                   (usuario, senha_hash, tipo))
    conexao.commit()
    cursor.close()
    conexao.close()

def login(usuario, senha):
    conexao = conectar()
    cursor = conexao.cursor()
    senha_hash = hash_senha(senha)
    cursor.execute("SELECT usuario, tipo FROM usuarios WHERE usuario=%s AND senha=%s",
                   (usuario, senha_hash))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado
