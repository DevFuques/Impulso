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
        user="fernando",        
        password="nandocafu",   
        database="academia"
    )

# Cria banco e tabela
def inicializa_banco():
    conexao = mysql.connect(
        host="localhost",
        user="fernando",
        password="nandocafu"
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
    conexao.commit()
    print("✅ BANCO/TABELA CRIADOS")
    cursor.close()
    conexao.close()

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
    
# Mostrar tabela
def exibir_tabela():
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
        print("\nNenhuma pessoa foi cadastrada!")
    
    cursor.close()
    conexao.close()
    
# Deletar pessoas da tabela
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

# Menu principal
def menu():
    inicializa_banco()
    
    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar pessoa")
        print("2 - Exibir pessoas cadastradas")
        print("3 - Mostrar médias")
        print("4 - Deletar cadastro")
        print("5 - Sair")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            cadastrar_pessoas()
        elif opcao == "2":
            exibir_tabela()
        elif opcao == "3":
            mostrar_medias()
        elif opcao == "4":
            deletar_cadastro()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("\n❌ Opção inválida, tente novamente!")

menu()
