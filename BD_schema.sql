-- Desabilita verificação de chaves estrangeiras temporariamente para permitir os DROPs
SET FOREIGN_KEY_CHECKS = 0;

-- 1. Limpeza (Ordem reversa de dependência ou brute force com FK check off)
DROP TABLE IF EXISTS Preferencia_Cliente;
DROP TABLE IF EXISTS Sessao_Visualizacao;
DROP TABLE IF EXISTS Disponibilidade_Filme;
DROP TABLE IF EXISTS Filme;
DROP TABLE IF EXISTS Catalogo_Regional;
DROP TABLE IF EXISTS Regiao_residencia;
DROP TABLE IF EXISTS Regiao;
DROP TABLE IF EXISTS Plano_Catalogo;
DROP TABLE IF EXISTS Catalogo;
DROP TABLE IF EXISTS Assina_Historico;
DROP TABLE IF EXISTS Plano;
DROP TABLE IF EXISTS Cliente;

-- 2. Criação das Tabelas Fortes

CREATE TABLE Cliente (
    CPF CHAR(11) PRIMARY KEY,
    nome_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_nasc DATE NOT NULL,
    pais VARCHAR(50) NOT NULL,
    data_cadastro DATE NOT NULL
);

CREATE TABLE Plano (
    ID_plano INT AUTO_INCREMENT PRIMARY KEY,
    nome_plano VARCHAR(50) NOT NULL,
    mensalidade DECIMAL(10, 2) NOT NULL,
    n_dispositivos INT NOT NULL,
    qualidade_max VARCHAR(20) NOT NULL -- Ex: 4K, 1080p
);

CREATE TABLE Catalogo (
    ID_Catalogo INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE Regiao (
    ID_regiao INT AUTO_INCREMENT PRIMARY KEY,
    Continente VARCHAR(50) NOT NULL,
    Pais VARCHAR(50) NOT NULL,
    Estado VARCHAR(50) NOT NULL
);

CREATE TABLE Filme (
    ID_filme INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    ano_lancamento INT NOT NULL,
    duracao INT NOT NULL, -- em minutos
    genero VARCHAR(50),
    classificacao_ind VARCHAR(10),
    produtora VARCHAR(100),
    idioma_original VARCHAR(50),
    sinopse TEXT
);

-- 3. Criação das Tabelas Associativas e Dependentes

CREATE TABLE Assina_Historico (
    CPF_cliente CHAR(11),
    ID_plano INT,
    data_inicio DATE NOT NULL,
    data_termino DATE, -- Pode ser NULL se for a assinatura atual
    PRIMARY KEY (CPF_cliente, ID_plano, data_inicio),
    FOREIGN KEY (CPF_cliente) REFERENCES Cliente(CPF),
    FOREIGN KEY (ID_plano) REFERENCES Plano(ID_plano)
);

CREATE TABLE Plano_Catalogo (
    ID_plano INT,
    ID_Catalogo INT,
    PRIMARY KEY (ID_plano, ID_Catalogo),
    FOREIGN KEY (ID_plano) REFERENCES Plano(ID_plano),
    FOREIGN KEY (ID_Catalogo) REFERENCES Catalogo(ID_Catalogo)
);

CREATE TABLE Regiao_residencia (
    CPF CHAR(11),
    ID_regiao INT,
    data_registro DATE NOT NULL,
    PRIMARY KEY (CPF, ID_regiao), -- Assumindo que o cliente tem uma residencia por regiao ou historico
    FOREIGN KEY (CPF) REFERENCES Cliente(CPF),
    FOREIGN KEY (ID_regiao) REFERENCES Regiao(ID_regiao)
);

CREATE TABLE Catalogo_Regional (
    ID_Catalogo INT,
    ID_regiao INT,
    PRIMARY KEY (ID_Catalogo, ID_regiao),
    FOREIGN KEY (ID_Catalogo) REFERENCES Catalogo(ID_Catalogo),
    FOREIGN KEY (ID_regiao) REFERENCES Regiao(ID_regiao)
);

CREATE TABLE Disponibilidade_Filme (
    ID_filme INT,
    ID_Catalogo INT,
    PRIMARY KEY (ID_filme, ID_Catalogo),
    FOREIGN KEY (ID_filme) REFERENCES Filme(ID_filme),
    FOREIGN KEY (ID_Catalogo) REFERENCES Catalogo(ID_Catalogo)
);

CREATE TABLE Sessao_Visualizacao (
    CPF_cliente CHAR(11),
    ID_filme INT,
    data_hora_inicio DATETIME NOT NULL,
    duracao_sessao INT NOT NULL, -- quantos minutos a pessoa assistiu
    dispositivo_utilizado VARCHAR(50), -- TV, Mobile, Web
    qualidade_reproducao VARCHAR(20),
    PRIMARY KEY (CPF_cliente, ID_filme, data_hora_inicio),
    FOREIGN KEY (CPF_cliente) REFERENCES Cliente(CPF),
    FOREIGN KEY (ID_filme) REFERENCES Filme(ID_filme)
);

CREATE TABLE Preferencia_Cliente (
    CPF_cliente CHAR(11),
    ID_filme INT,
    favorito_bool BOOLEAN DEFAULT FALSE,
    avaliacao INT CHECK (avaliacao BETWEEN 1 AND 5),
    data_interacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (CPF_cliente, ID_filme),
    FOREIGN KEY (CPF_cliente) REFERENCES Cliente(CPF),
    FOREIGN KEY (ID_filme) REFERENCES Filme(ID_filme)
);

-- Reabilita verificação
SET FOREIGN_KEY_CHECKS = 1;