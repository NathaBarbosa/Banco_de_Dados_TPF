import os
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from random import choice, sample
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
    """Gera um CPF fictício de 11 dígitos"""
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
    print("Recriando estrutura do banco...")
    nome_arquivo = 'BD_schema.sql' 
    
    if not os.path.exists(nome_arquivo):
        print(f"ERRO CRÍTICO: O arquivo '{nome_arquivo}' não foi encontrado!")
        exit()

    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        sql_file = f.read()
        commands = sql_file.split(';')
        for command in tqdm(commands, desc="Executando DDL"):
            if command.strip():
                try:
                    cursor.execute(command)
                except Error as e:
                    print(f"Erro SQL ignorado: {e}")

def inserir_em_lotes(cursor, sql, dados, tamanho_lote=5000, descricao="Inserindo"):
    """Função para inserir grandes quantidades de dados em pedaços menores com barra de progresso"""
    total = len(dados)
   
    for i in tqdm(range(0, total, tamanho_lote), desc=f"{descricao}", leave=False):
        lote = dados[i:i + tamanho_lote]
        cursor.executemany(sql, lote)
        
def escolher_idioma():
    IDIOMAS = {
        "Inglês": 0.45,
        "Espanhol": 0.10,
        "Português": 0.10,
        "Francês": 0.05,
        "Alemão": 0.04,
        "Italiano": 0.04,
        "Japonês": 0.05,
        "Coreano": 0.05,
        "Chinês (Mandarim)": 0.05,
        "Hindi": 0.03
    }
    
    r = random.random()
    acumulado = 0
    for idioma, peso in IDIOMAS.items():
        acumulado += peso
        if r <= acumulado:
            return idioma
        
    return "Inglês"

# --- Funções de População ---

def popular_planos(cursor):
    print("Inserindo Planos...")
    planos = [
        ("Mobile", 19.90, 1, "480p"),
        ("Básico", 29.90, 2, "1080p"),
        ("Padrão", 45.90, 3, "4K"),
        ("Premium", 59.90, 4, "4K+HDR")
    ]
    cursor.executemany("INSERT INTO Plano (nome_plano, mensalidade, n_dispositivos, qualidade_max) VALUES (%s, %s, %s, %s)", planos)

def popular_regioes(cursor):
    print("Inserindo Regiões...")
    
    regioes = [
        # América do Sul
        ("América do Sul", "Brasil", "São Paulo"),
        ("América do Sul", "Brasil", "Amazonas"),
        ("América do Sul", "Brasil", "Bahia"),
        ("América do Sul", "Argentina", "Buenos Aires"),
        ("América do Sul", "Chile", "Santiago"),
        ("América do Sul", "Colômbia", "Bogotá"),

        # América do Norte
        ("América do Norte", "Estados Unidos", "California"),
        ("América do Norte", "Estados Unidos", "Texas"),
        ("América do Norte", "Estados Unidos", "Nova York"),
        ("América do Norte", "Canadá", "Ontario"),
        ("América do Norte", "Canadá", "Quebec"),
        ("América do Norte", "México", "Jalisco"),

        # Europa
        ("Europa", "França", "Île-de-France"),
        ("Europa", "Alemanha", "Baviera"),
        ("Europa", "Reino Unido", "Inglaterra"),
        ("Europa", "Portugal", "Lisboa"),
        ("Europa", "Espanha", "Catalunha"),
        ("Europa", "Itália", "Lombardia"),

        # Ásia
        ("Ásia", "Japão", "Tóquio"),
        ("Ásia", "China", "Pequim"),
        ("Ásia", "Índia", "Maharashtra"),
        ("Ásia", "Coreia do Sul", "Seul"),
        ("Ásia", "Arábia Saudita", "Riyadh"),
        ("Ásia", "Indonésia", "Java Ocidental"),

        # África
        ("África", "Nigéria", "Lagos"),
        ("África", "África do Sul", "Gauteng"),
        ("África", "Egito", "Cairo"),
        ("África", "Quênia", "Nairóbi"),
        ("África", "Marrocos", "Casablanca"),

        # Oceania
        ("Oceania", "Austrália", "Nova Gales do Sul"),
        ("Oceania", "Austrália", "Victoria"),
        ("Oceania", "Nova Zelândia", "Auckland")
    ]

    cursor.executemany(
        "INSERT INTO Regiao (Continente, Pais, Estado) VALUES (%s, %s, %s)",
        regioes
    )

def popular_catalogos(cursor):
    print("Inserindo Catálogos...")

    catalogos = [
        # Catálogos gerais
        ("Catálogo Global",),
        ("Catálogo Internacional",),
        ("Catálogo Latam",),
        ("Catálogo Europa",),
        ("Catálogo Ásia e Oceania",),

        # Conteúdos originais e exclusivos
        ("Originais Exclusivos",),
        ("Produções Independentes",),
        ("Conteúdos Premium",)
    ]

    cursor.executemany(
        "INSERT INTO Catalogo (descricao) VALUES (%s)",
        catalogos
    )

def popular_filmes(cursor, qtd):
    print(f"Gerando {qtd} Filmes...")
    generos = [
        "Ação", "Aventura", "Comédia", "Comédia Romântica", "Drama", "Terror",
        "Suspense", "Sci-Fi", "Fantasia", "Documentário", "Biografia",
        "Romance", "Animação", "Musical", "Crime", "Guerra", "Histórico",
        "Western", "Mistério", "Esportes"
    ]
    classificacoes = ["Livre", "10", "12", "14", "16", "18"]
    
    dados = []
    # Loop de GERAÇÃO
    for _ in tqdm(range(qtd), desc="Gerando Filmes"):
        titulo = fake.catch_phrase().title() 
        ano = random.randint(1990, 2024)
        duracao = random.randint(80, 180)
        genero = random.choice(generos)
        classif = random.choice(classificacoes)
        produtora = fake.company()
        idioma = escolher_idioma()
        sinopse = fake.text(max_nb_chars=200)
        
        dados.append((titulo, ano, duracao, genero, classif, produtora, idioma, sinopse))
    
    sql = """INSERT INTO Filme (titulo, ano_lancamento, duracao, genero, classificacao_ind, produtora, idioma_original, sinopse) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""          
    inserir_em_lotes(cursor, sql, dados, descricao="Filmes")

def popular_clientes(cursor, qtd):
    PAISES_LOCAIS = {
        "Brasil": "pt_BR",
        "Estados Unidos": "en_US",
        "Canadá": "en_CA",
        "México": "es_MX",
        "Argentina": "es_AR",
        "Chile": "es_CL",
        "Portugal": "pt_PT",
        "Espanha": "es_ES",
        "Reino Unido": "en_GB",
        "França": "fr_FR",
        "Alemanha": "de_DE",
        "Itália": "it_IT",
        "Japão": "ja_JP",
        "China": "zh_CN",
        "Coreia do Sul": "ko_KR",
        "Índia": "en_IN",
        "Austrália": "en_AU"
    }
    
    print(f"Gerando {qtd} Clientes...")
    dados = []
    cpfs_gerados = []

    # Loop de GERAÇÃO
    for _ in tqdm(range(qtd), desc="Gerando Clientes"):
        # Sorteia país
        pais = choice(list(PAISES_LOCAIS.keys()))
        # Define o Faker com o locale adequado
        fake_local = Faker(PAISES_LOCAIS[pais])
        cpf = gerar_cpf()  
        cpfs_gerados.append(cpf)
        nome = fake_local.name()
        email = f"{fake_local.user_name()}_{random.randint(1,999)}@email.com"
        nasc = fake_local.date_of_birth(minimum_age=16, maximum_age=70)
        cadastro = fake_local.date_between(start_date='-5y', end_date='today')
        dados.append((cpf, nome, email, nasc, pais, cadastro))

    sql = """
        INSERT INTO Cliente (CPF, nome_completo, email, data_nasc, pais, data_cadastro)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    inserir_em_lotes(cursor, sql, dados, descricao="Clientes")
    return cpfs_gerados

def popular_associativas_e_historico(cursor, cpfs):
    print("Criando relacionamentos dinâmicos...")
    
    # Carrega IDs para uso aleatório
    cursor.execute("SELECT ID_plano FROM Plano")
    ids_plano = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT ID_regiao FROM Regiao")
    ids_regiao = [r[0] for r in cursor.fetchall()]

    cursor.execute("SELECT ID_filme, duracao FROM Filme")
    filmes = cursor.fetchall()

    cursor.execute("SELECT ID_Catalogo FROM Catalogo")
    ids_catalogo = [r[0] for r in cursor.fetchall()]

    if not ids_plano or not ids_regiao or not filmes or not ids_catalogo:
        print("ERRO: Tabelas base vazias. Popule-as primeiro.")
        return

    # 1. Clientes, Regiões e Assinaturas
    residencia_data = []
    assinatura_data = []

    for cpf in tqdm(cpfs, desc="Associando Dados"):
        regiao = choice(ids_regiao) 
        residencia_data.append((cpf, regiao, fake.date_between(start_date='-3y')))

        if random.random() > 0.10: # 90% assinam
            plano = choice(ids_plano)
            inicio = fake.date_between(start_date='-2y')
            fim = fake.date_between(start_date=inicio) if random.random() < 0.25 else None
            assinatura_data.append((cpf, plano, inicio, fim))

    inserir_em_lotes(cursor, "INSERT INTO Regiao_residencia (CPF, ID_regiao, data_registro) VALUES (%s, %s, %s)", residencia_data, descricao="Residências")
    inserir_em_lotes(cursor, "INSERT INTO Assina_Historico (CPF_cliente, ID_plano, data_inicio, data_termino) VALUES (%s, %s, %s, %s)", assinatura_data, descricao="Assinaturas")

    # 2. Distribuição de Catálogos (Regiões e Planos)
    print()#Quebra de linha para melhor visualização
    cat_reg_data = []
    plano_cat_data = []
    
    for id_cat in tqdm(ids_catalogo, desc="Distribuindo Catálogos"):
        regioes_sorteadas = sample(ids_regiao, k=random.randint(2, len(ids_regiao)))
        for reg in regioes_sorteadas:
            cat_reg_data.append((id_cat, reg))
    
    for id_plano in ids_plano:
        catalogos_sorteados = sample(ids_catalogo, k=random.randint(1, len(ids_catalogo)))
        for cat in catalogos_sorteados:
            plano_cat_data.append((id_plano, cat))

    inserir_em_lotes(cursor, "INSERT IGNORE INTO Catalogo_Regional (ID_Catalogo, ID_regiao) VALUES (%s, %s)", cat_reg_data, descricao="Catálogos Regionais")
    inserir_em_lotes(cursor, "INSERT IGNORE INTO Plano_Catalogo (ID_plano, ID_Catalogo) VALUES (%s, %s)", plano_cat_data, descricao="Planos x Catálogos")

    # 3. Disponibilidade de Filmes
    print()#Quebra de linha para melhor visualização
    disp_data = []
    for f in tqdm(filmes, desc="Distribuindo Filmes"):
        cats_filme = sample(ids_catalogo, k=random.randint(1, min(3, len(ids_catalogo))))
        for cat in cats_filme:
            disp_data.append((f[0], cat))

    inserir_em_lotes(cursor, "INSERT IGNORE INTO Disponibilidade_Filme (ID_filme, ID_Catalogo) VALUES (%s, %s)", disp_data, descricao="Disponibilidade")

    # 4. Sessões e Preferências
    print()#Quebra de linha para melhor visualização
    sessoes_data = []
    prefs_data = []

    for cpf in tqdm(cpfs, desc="Gerando Histórico"):
        qtd_sessoes = random.randint(5, 40)

        for _ in range(qtd_sessoes):
            filme = choice(filmes)
            id_filme, duracao_total = filme[0], filme[1]

            inicio = fake.date_time_between(start_date='-6m', end_date='now')
            progresso = random.randint(5, duracao_total)
            dispositivo = choice(["TV", "Celular", "Web", "Tablet"])
            qualidade = choice(["HD", "4K"])

            sessoes_data.append((cpf, id_filme, inicio, progresso, dispositivo, qualidade))

            if progresso > duracao_total * 0.8 and random.random() > 0.5:
                prefs_data.append((cpf, id_filme, choice([True, False]), random.randint(1, 5), inicio))

    inserir_em_lotes(cursor, "INSERT IGNORE INTO Sessao_Visualizacao (CPF_cliente, ID_filme, data_hora_inicio, duracao_sessao, dispositivo_utilizado, qualidade_reproducao) VALUES (%s, %s, %s, %s, %s, %s)", sessoes_data, descricao="Sessões")
    inserir_em_lotes(cursor, "INSERT IGNORE INTO Preferencia_Cliente (CPF_cliente, ID_filme, favorito_bool, avaliacao, data_interacao) VALUES (%s, %s, %s, %s, %s)", prefs_data, descricao="Avaliações")
     
    print(f"✔ Sessões inseridas: {len(sessoes_data)}")

    print(f"✔ Avaliações inseridas: {len(prefs_data)}")

    print("Dados gerados com maior realismo e variabilidade!")

def main():
    conn = criar_conexao()
    if conn:
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            
            resetar_banco(cursor)
            
            # Dados Fixos
            popular_planos(cursor)
            popular_regioes(cursor)
            popular_catalogos(cursor)
            
            # Dados Volumosos (Escalados para realismo)
            
            popular_filmes(cursor, qtd=1000)
            
            cpfs = popular_clientes(cursor, qtd=3000)
            
            
            popular_associativas_e_historico(cursor, cpfs)
            
            conn.commit()
            print("\n" + "="*50)
            print("SUCESSO! Banco populado com ALTO VOLUME de dados.")
            print("="*50)
            
        except Exception as e:
            print(f"\nErro fatal: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    main()
