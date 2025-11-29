import os
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime, timedelta
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# Configuração
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'meu_banco_trabalho'),
    'user': os.getenv('DB_USER', 'aluno'),
    'password': os.getenv('DB_PASSWORD', 'senha_segura'),
    'port': int(os.getenv('DB_PORT', 3306))
}

fake = Faker('pt_BR')

# --- Funções Auxiliares ---
def gerar_cpf():
    """Gera um CPF fictício de 11 dígitos (apenas números)"""
    return str(fake.unique.random_number(digits=11, fix_len=True))

def criar_conexao():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro de conexão: {e}")
    return None

def resetar_banco(cursor):
    print("Recriando tabelas...")
    try:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            sql_file = f.read()
            commands = sql_file.split(';')
            for command in tqdm(commands, desc="DDL"):
                if command.strip():
                    try:
                        cursor.execute(command)
                    except Error as e:
                        print(f"Erro SQL (ignorado): {e}")
    except FileNotFoundError:
        print("ERRO: Arquivo 'schema.sql' não encontrado na pasta.")

# --- Funções de População (Sementes) ---

def popular_planos(cursor):
    print("Inserindo Planos...")
    planos = [
        ("Mobile", 19.90, 1, "480p"),
        ("Básico", 29.90, 2, "1080p"),
        ("Padrão", 45.90, 2, "4K"),
        ("Premium", 59.90, 4, "4K+HDR")
    ]
    cursor.executemany("INSERT INTO Plano (nome_plano, mensalidade, n_dispositivos, qualidade_max) VALUES (%s, %s, %s, %s)", planos)

def popular_regioes(cursor):
    print("Inserindo Regiões...")
    regioes = [
        ("América do Sul", "Brasil", "São Paulo"),
        ("América do Sul", "Brasil", "Rio de Janeiro"),
        ("América do Norte", "Estados Unidos", "California"),
        ("Europa", "França", "Île-de-France"),
        ("Ásia", "Japão", "Tóquio")
    ]
    cursor.executemany("INSERT INTO Regiao (Continente, Pais, Estado) VALUES (%s, %s, %s)", regioes)

def popular_catalogos(cursor):
    print("Inserindo Catálogos...")
    # CORREÇÃO AQUI: A vírgula no final da tupla ("Item",) é obrigatória para tuplas de um elemento
    catalogos = [
        ("Catálogo Global",), 
        ("Catálogo Latam",), 
        ("Originais Exclusivos",), 
        ("Clássicos Cult",)
    ]
    cursor.executemany("INSERT INTO Catalogo (descricao) VALUES (%s)", catalogos)

def popular_filmes(cursor, qtd=50):
    print(f"Gerando {qtd} Filmes...")
    generos = ["Ação", "Comédia", "Drama", "Terror", "Sci-Fi", "Documentário"]
    classificacoes = ["Livre", "10", "12", "14", "16", "18"]
    
    dados = []
    for _ in range(qtd):
        titulo = fake.catch_phrase().title() 
        ano = random.randint(1980, 2024)
        duracao = random.randint(80, 180)
        genero = random.choice(generos)
        classif = random.choice(classificacoes)
        produtora = fake.company()
        idioma = "Inglês" if random.random() > 0.3 else "Português"
        sinopse = fake.text(max_nb_chars=200)
        
        dados.append((titulo, ano, duracao, genero, classif, produtora, idioma, sinopse))
    
    sql = """INSERT INTO Filme (titulo, ano_lancamento, duracao, genero, classificacao_ind, produtora, idioma_original, sinopse) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.executemany(sql, dados)

# --- Funções de População (Dinâmicas) ---

def popular_clientes(cursor, qtd=100):
    print(f"Gerando {qtd} Clientes...")
    dados = []
    cpfs_gerados = []
    
    for _ in tqdm(range(qtd), desc="Clientes"):
        cpf = gerar_cpf()
        cpfs_gerados.append(cpf)
        nome = fake.name()
        email = fake.unique.email()
        nasc = fake.date_of_birth(minimum_age=16, maximum_age=70)
        pais = "Brasil"
        cadastro = fake.date_between(start_date='-5y', end_date='today')
        
        dados.append((cpf, nome, email, nasc, pais, cadastro))
        
    sql = "INSERT INTO Cliente (CPF, nome_completo, email, data_nasc, pais, data_cadastro) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(sql, dados)
    return cpfs_gerados

def popular_associativas(cursor, cpfs):
    print("Populando tabelas associativas e histórico...")
    
    cursor.execute("SELECT ID_plano FROM Plano")
    ids_plano = [r[0] for r in cursor.fetchall()]
    
    cursor.execute("SELECT ID_regiao FROM Regiao")
    ids_regiao = [r[0] for r in cursor.fetchall()]
    
    cursor.execute("SELECT ID_filme, duracao FROM Filme")
    filmes = cursor.fetchall() 
    
    cursor.execute("SELECT ID_Catalogo FROM Catalogo")
    ids_catalogo = [r[0] for r in cursor.fetchall()]

    if not ids_plano or not ids_regiao or not filmes:
        print("ERRO CRÍTICO: Tabelas base (Plano, Regiao, Filme) parecem vazias.")
        return

    # 1. Regiao_residencia
    residencia_data = []
    for cpf in cpfs:
        residencia_data.append((cpf, random.choice(ids_regiao), fake.date_between(start_date='-2y')))
    cursor.executemany("INSERT INTO Regiao_residencia (CPF, ID_regiao, data_registro) VALUES (%s, %s, %s)", residencia_data)

    # 2. Assina_Historico
    assinatura_data = []
    for cpf in cpfs:
        if random.random() > 0.2:
            plano = random.choice(ids_plano)
            inicio = fake.date_between(start_date='-1y')
            fim = None
            if random.random() < 0.2:
                fim = fake.date_between(start_date=inicio)
            assinatura_data.append((cpf, plano, inicio, fim))
    cursor.executemany("INSERT INTO Assina_Historico (CPF_cliente, ID_plano, data_inicio, data_termino) VALUES (%s, %s, %s, %s)", assinatura_data)

    # 3. Catalogo_Regional e Plano_Catalogo
    for id_cat in ids_catalogo:
        cursor.execute("INSERT IGNORE INTO Catalogo_Regional (ID_Catalogo, ID_regiao) VALUES (%s, %s)", (id_cat, ids_regiao[0]))
        cursor.execute("INSERT IGNORE INTO Plano_Catalogo (ID_plano, ID_Catalogo) VALUES (%s, %s)", (ids_plano[0], id_cat))
        
    # 4. Disponibilidade_Filme
    disp_data = []
    if ids_catalogo:
        cat_global = ids_catalogo[0]
        for filme in filmes:
            disp_data.append((filme[0], cat_global))
        cursor.executemany("INSERT INTO Disponibilidade_Filme (ID_filme, ID_Catalogo) VALUES (%s, %s)", disp_data)

    # 5. Sessao_Visualizacao e Preferencia
    print("Gerando visualizações e avaliações...")
    sessoes_data = []
    prefs_data = []
    
    for _ in tqdm(range(300), desc="Sessões"): 
        cpf = random.choice(cpfs)
        filme = random.choice(filmes)
        id_filme = filme[0]
        duracao_total = filme[1]
        
        inicio = fake.date_time_between(start_date='-6m')
        duracao_assistida = random.randint(1, duracao_total)
        device = random.choice(["Smart TV", "Smartphone", "Web Browser", "Tablet"])
        qualidade = random.choice(["HD", "4K", "SD"])
        
        sessoes_data.append((cpf, id_filme, inicio, duracao_assistida, device, qualidade))
        
        if random.random() > 0.7:
            favorito = random.choice([True, False])
            nota = random.randint(1, 5)
            prefs_data.append((cpf, id_filme, favorito, nota, inicio))

    cursor.executemany("INSERT INTO Sessao_Visualizacao (CPF_cliente, ID_filme, data_hora_inicio, duracao_sessao, dispositivo_utilizado, qualidade_reproducao) VALUES (%s, %s, %s, %s, %s, %s)", sessoes_data)
    
    for p in prefs_data:
        try:
            cursor.execute("INSERT INTO Preferencia_Cliente (CPF_cliente, ID_filme, favorito_bool, avaliacao, data_interacao) VALUES (%s, %s, %s, %s, %s)", p)
        except Error:
            pass 

def main():
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            
            resetar_banco(cursor)
            
            popular_planos(cursor)
            popular_regioes(cursor)
            popular_catalogos(cursor)
            popular_filmes(cursor, qtd=50)
            
            cpfs = popular_clientes(cursor, qtd=100)
            popular_associativas(cursor, cpfs)
            
            conn.commit()
            print("\n" + "="*50)
            print(" SUCESSO! Banco de dados populado com dados falsos. 🎬")
            print("="*50)
            
        except Exception as e:
            print(f"\nErro fatal: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()