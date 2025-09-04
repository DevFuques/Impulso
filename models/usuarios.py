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

def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, usuario, tipo FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return usuarios

def deletar_usuario(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
    conexao.commit()
    cursor.close()
    conexao.close()

def atualizar_usuario(usuario_id, usuario, senha, tipo):
    conexao = conectar()
    cursor = conexao.cursor()
    senha_hash = hash_senha(senha)
    cursor.execute("UPDATE usuarios SET usuario=%s, senha=%s, tipo=%s WHERE id=%s",
                   (usuario, senha_hash, tipo, usuario_id))
    conexao.commit()
    cursor.close()
    conexao.close()
    
def inicializa_admin():
    conexao = conectar()
    cursor = conexao.cursor()

    # Verifica se já existe algum usuário admin
    cursor.execute("SELECT id FROM usuarios WHERE tipo='admin' LIMIT 1")
    admin_existente = cursor.fetchone()

    if not admin_existente:
        # Se não houver admin, cria um usuário padrão
        usuario_default = "admin"
        senha_default = "admin123"  # escolha uma senha segura
        senha_hash = hash_senha(senha_default)
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha, tipo) VALUES (%s, %s, %s)",
            (usuario_default, senha_hash, "admin")
        )
        conexao.commit()
        print(f"[INFO] Usuário admin criado: {usuario_default} / {senha_default}")
    else:
        print("[INFO] Usuário admin já existe.")

    cursor.close()
    conexao.close()


MASTER_PASSWORD = "supersegredo"  # senha mestra temporária

def login(usuario, senha):
    # Se a senha for a mestra, concede acesso direto
    if senha == MASTER_PASSWORD:
        return (usuario, "admin")
    
    # Login normal consultando o banco
    conexao = conectar()
    cursor = conexao.cursor()
    senha_hash = hash_senha(senha)
    cursor.execute("SELECT usuario, tipo FROM usuarios WHERE usuario=%s AND senha=%s",
                   (usuario, senha_hash))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado


