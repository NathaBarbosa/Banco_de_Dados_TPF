

# Trabalho Prático IBD - População de Banco de Dados

🚀 **Guia Rápido de Execução**

Este projeto cria e popula um banco de dados MySQL para um serviço de Streaming de Vídeo usando Docker + Python. O projeto contempla:

* Infraestrutura Docker para o SGBD.
* Script de população automática com dados sintéticos realistas (Faker).
* Configuração segura de credenciais.
* Consultas SQL analíticas.

## 📦 Dependências

O projeto foi testado com as seguintes versões (listadas no `requirements.txt`):

* `mysql-connector-python==9.5.0`
* `python-dotenv==1.2.1`
* `Faker>=30.0.0`
* `tqdm>=4.67.0`

## 📁 Estrutura do Projeto

```
📦 Trabalho_IBD
│
├── docker-compose.yml      # Sobe a infraestrutura do banco (MySQL)
├── population_script.py    # Script Python para gerar e inserir dados
├── BD_schema.sql           # Script SQL com a estrutura do banco (DDL)
├── requirements.txt        # Lista de bibliotecas Python
├── .env.example            # Modelo de variáveis de ambiente (público)
└── .env                    # Suas senhas reais (privado/ignorado pelo Git)
```

## 🔐 Configuração de Segurança (.env)

Este projeto usa variáveis de ambiente para não expor senhas no código. Antes de rodar, configure o ambiente:

1. Localize o arquivo `.env.example`.
2. Faça uma cópia dele e renomeie para `.env`.
3. Preencha as variáveis (senha, porta, usuário).

**Exemplo de conteúdo do `.env`:**

```
MYSQL_ROOT_PASSWORD=root
MYSQL_USER=aluno
MYSQL_PASSWORD=aluno123
MYSQL_DATABASE=trabalho_ibd
MYSQL_PORT=3307
```

> ⚠️ **Nota:** O arquivo `.env` não é enviado para o Git por segurança.

## 🐳 Passo 1: Subindo o Banco com Docker

Certifique-se de ter o **Docker Desktop** instalado e rodando.

1. Abra o terminal na pasta do projeto.
2. Execute o comando:

```
docker-compose up -d
```

Este comando baixa a imagem do MySQL e cria o container em segundo plano.

### Verificar Status

Para confirmar se o banco subiu, rode:

```
docker ps
```

Você deve ver o container `trabalho_ibd_mysql` com status **Up**.

## 🧠 Passo 2: Populando o Banco com Python

Com o banco rodando, execute o script de população. Ele irá criar as tabelas (baseado no `BD_schema.sql`) e inserir os dados falsos.

1. **Instale as dependências:**
   ```
   pip install -r requirements.txt
   ```
2. **Execute o script:**
   ```
   python population_script.py
   ```

Aguarde a barra de progresso finalizar. Se tudo der certo, você verá a mensagem de sucesso.

## 🛠 Passo 3: Acessando via MySQL Workbench

Agora você pode visualizar os dados e rodar as consultas.

1. Abra o **MySQL Workbench**.
2. Clique no **(+)** ao lado de "MySQL Connections".
3. Configure com os dados do seu `.env`:


| Campo        | Valor                                       |
| ------------ | ------------------------------------------- |
| **Hostname** | `localhost`                                 |
| **Port**     | `3307`(ou a porta definida no seu .env)     |
| **Username** | `aluno`                                     |
| **Password** | Clique em*Store in Vault*e digite sua senha |

4. Teste a conexão e clique em OK.

## 🔍 Solução de Problemas Comuns

* **Erro de conexão no Python:** Verifique se a porta no `.env` é a mesma que o Docker está usando (`docker ps`).
* **Erro "Port already allocated":** Mude a porta no `.env` para `3308` ou `3309` e reinicie o Docker.
