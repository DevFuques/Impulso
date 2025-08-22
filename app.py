import hashlib

# Função para gerar hash da senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Tenta usar mysql-connector, caso se não tenha tenta o PyMySQL
try:
    import mysql.connector as mysql
    print("✅ Usando mysql-connector-python")
except ImportError:
    import pymysql as mysql
    print("✅ Usando PyMySQL")

# Função de conexão
def conectar():
    return mysql.connect(
        host="localhost",
        user="root",        # substitua pelo seu usuário do MySQL
        password="senha",   # substitua pela sua senha do MySQL   
        database="academia"
    )

# Cria banco e tabelas
def inicializa_banco():
    conexao = mysql.connect(
        host="localhost",
        user="root",     # substitua pelo seu usuário do MySQL
        password="senha" # substitua pela sua senha do MySQL
    )
    cursor = conexao.cursor()
    cursor.execute("create database if not exists academia")
    cursor.execute("USE academia")

    cursor.execute("""
        create table if not exists pessoas (
            id int auto_increment primary key, 
            nome varchar(255),
            idade int,
            peso float
        )
    """)

    cursor.execute("""
        create table if not exists usuarios(
            id int auto_increment primary key,
            usuario varchar(50) unique not null,
            senha varchar(64) not null,
            tipo varchar(20) not null default 'usuario'
        )
    """)
    
    # cria admin padrão se não existir
    cursor.execute("select count(*) from usuarios")
    if cursor.fetchone()[0] == 0:
        senha_hash = hash_senha("admin")
        cursor.execute(
            "insert into usuarios (usuario, senha, tipo) values (%s, %s, %s)",
            ("admin", senha_hash, "admin")
        )
        print("⭐ Usuário admin criado (usuario: admin | senha: admin)")

    conexao.commit()
    print("✅ BANCO/TABELAS CRIADOS")
    cursor.close()
    conexao.close()
    
# Cadastrar novo usuário
def cadastrar_usuario():
    conexao = conectar()
    cursor = conexao.cursor()
    
    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    senha_hash = hash_senha(senha)

    tipo = input("Tipo de usuário (admin/usuario): ").lower()
    if tipo not in ["admin", "usuario"]:
        tipo = "usuario"  # se não digitar certo, vira usuário comum

    try:
        cursor.execute("insert into usuarios (usuario, senha, tipo) values (%s, %s, %s)", 
                       (usuario, senha_hash, tipo))
        conexao.commit()
        print(f"✅ Usuário {usuario} cadastrado como {tipo}!")
    except mysql.Error as e:
        print(f"❌ Erro: {e}")

    cursor.close()
    conexao.close()

    
# Login
def login():
    conexao = conectar()
    cursor = conexao.cursor()
    
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    senha_hash = hash_senha(senha)

    cursor.execute("select usuario, tipo from usuarios where usuario=%s and senha=%s", (usuario, senha_hash))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        print(f"\n✅ Olá, {resultado[0]}! (Tipo: {resultado[1]})")
        return resultado[1] 
    else:
        print("\n❌ Usuário ou senha inválidos!")
        return None


# Inserir pessoa
def cadastrar_pessoas():
    conexao = conectar()
    cursor = conexao.cursor()
    
    nome = input("Digite o nome: ")
    idade = int(input("Digite a idade: "))
    peso = float(input("Digite o peso: "))
    sql = "insert into pessoas (nome, idade, peso) values (%s, %s, %s)"
    
    cursor.execute(sql, (nome, idade, peso))
    conexao.commit()
    
    print("✅ PESSOA CADASTRADA")
    
    cursor.close()
    conexao.close()

# Mostrar médias
def mostrar_medias():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("select avg(idade), avg(peso) from pessoas")
    
    media_idade, media_peso = cursor.fetchone()
    
    print(f"\nMédia de idade: {media_idade:.2f} anos")
    print(f"Média de peso: {media_peso:.2f} kg\n")
    
    cursor.close()
    conexao.close()
    
# Mostrar tabela pessoas
def exibir_tab_pes():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("select * from pessoas")
    linhas = cursor.fetchall()
    
    if linhas:
        print("\n=== PESSOAS CADASTRADAS ===")
        for linha in linhas:
            print("---" * 10)
            print(f"| ID: {linha[0]} | Nome: {linha[1]} | Idade: {linha[2]} | Peso: {linha[3]} |")
    else:
        print("\n❌ Nenhuma pessoa foi cadastrada!")
    
    cursor.close()
    conexao.close()
    
# Mostrar tabela usuarios
def exibir_tab_user():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("select * from pessoas")
    linhas = cursor.fetchall()
    
    if linhas:
        print("\n=== USUÁRIOS CADASTRADOS ===")
        for linha in linhas:
            print("---" * 10)
            print(f"| ID: {linha[0]} | Usuário: {linha[1]} | Tipo: {linha[3]} |")
    else:
        print("\n❌ Nenhum usuário foi cadastrado!")
    
    cursor.close()
    conexao.close()
    
# Deletar pessoas da tabela pessoas
def deletar_cadastro():
    conexao = conectar()
    cursor = conexao.cursor()
    
    id_pessoa = int(input("Digite o ID da pessoa a ser deletada: "))
    sql = "delete from pessoas where id = %s"
    
    cursor.execute(sql, (id_pessoa,))
    conexao.commit()
    
    if cursor.rowcount > 0:
        print("\n✅ CADASTRO DELETADO")
    else:
        print("\n❌ ID não encontrado!")
    
    cursor.close()
    conexao.close()

# Deletar usuarios da tabela usuarios
def deletar_usuario():
    conexao = conectar()
    cursor = conexao.cursor()
    
    id_usuario = int(input("Digite o ID do usuario a ser deletada: "))
    sql = "delete from pessoas where id = %s"
    
    cursor.execute(sql, (id_usuario,))
    conexao.commit()
    
    if cursor.rowcount > 0:
        print("\n✅ USUÁRIO DELETADO")
    else:
        print("\n❌ ID não encontrado!")
    
    cursor.close()
    conexao.close()


# Menu principal
def menu(tipo_usuario):
    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar pessoa")
        print("2 - Exibir pessoas cadastradas")
        print("3 - Mostrar médias(idade e peso)")
        print("4 - Deletar cadastro")

        # só admin pode criar, exibir ou deletar novos usuários
        if tipo_usuario == "admin":
            print("5 - Cadastrar novo usuário")
            print("6 - Exibir usuários cadastrados")
            print("7 - Deletar usuário")

        print("0 - Sair")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            cadastrar_pessoas()
        elif opcao == "2":
            exibir_tab_pes()
        elif opcao == "3":
            mostrar_medias()
        elif opcao == "4":
            deletar_cadastro()
        elif opcao == "5" and tipo_usuario == "admin":
            cadastrar_usuario()
        elif opcao == "6" and tipo_usuario == "admin":
            exibir_tab_user()
        elif opcao == "7" and tipo_usuario == "admin":
            deletar_usuario()
        elif opcao == "0":
            print("Obrigado por usar o sistema IMPULSO, saindo...")
            break
        else:
            print("\n❌ Opção inválida, tente novamente!")


# Programa principal
def main():
    inicializa_banco()
    print("\n=== IMPULSO ===")
    
    tipo_usuario = login()
    if tipo_usuario: 
        menu(tipo_usuario)
    else:
        print("\nEncerrando o programa...")

main()
