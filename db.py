try:
    import mysql.connector as mysql
    print("✅ Usando mysql-connector-python")
except ImportError:
    try:
        import pymysql as mysql
        print("✅ Usando PyMySQL")
    except ImportError:
        raise ImportError("❌ Nenhuma biblioteca MySQL encontrada! "
                          "Instale com: pip install mysql-connector-python ou pip install pymysql")

def conectar():
    return mysql.connect(
        host="localhost",
        user="root",        # Ajuste conforme seu usuário do MySQL
        password="senha",   # Ajuste conforme sua senha do MySQL
        database="academia"
    )

def inicializa_banco():
    conexao = mysql.connect(
        host="localhost",
        user="root",        # Ajuste conforme seu usuário do MySQL
        password="senha"    # Ajuste conforme sua senha do MySQL
    )
    cursor = conexao.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS academia")
    cursor.execute("USE academia")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            idade INT,
            peso FLOAT,
            cep VARCHAR(10),
            logradouro VARCHAR(255),
            bairro VARCHAR(255),
            cidade VARCHAR(100),
            estado VARCHAR(2)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(50) UNIQUE NOT NULL,
            senha VARCHAR(64) NOT NULL,
            tipo VARCHAR(20) NOT NULL DEFAULT 'usuario'
        )
    """)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("✅ Banco e tabelas prontos!")
