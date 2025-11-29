🚀 Guia Rápido de Execução — Trabalho Prático IBD

Este projeto cria e popula um banco de dados MySQL usando Docker + Python.
Ele contém:

Um script de infraestrutura Docker para subir o banco.

Um script de população automática com dados sintéticos.

Arquivos de configuração para controle seguro das credenciais.

Um script SQL com o esquema do banco.

Após seguir os passos, você terá o banco configurado e pronto para consultas no MySQL Workbench.

📦 Dependências

O projeto utiliza as seguintes bibliotecas Python:
mysql-connector-python==9.5.0
python-dotenv==1.2.1
Faker>=30.0.0
tqdm>=4.67.0


📁 Estrutura do Projeto
📦 Trabalho_IBD
│
├── docker-compose.yml       # Sobe a infraestrutura do banco (MySQL)
├── population_script.py     # Script em Python para gerar dados
├── BD_schema.sql            # Estrutura do banco (DDL)
├── .env.example             # Modelo de variáveis de ambiente
├── .env   (criado pelo usuário)
└── requirements.txt         # Dependências Python

🔐 Arquivo .env — Configuração de Segurança

Antes de qualquer execução, configure o ambiente:

Localize o arquivo: .env.example

Faça uma cópia com o nome: .env

Preencha as variáveis nele (password, porta, usuário etc.).

⚠️ O .env não vai para o Git, garantindo segurança das credenciais.

Exemplo comum de conteúdo:

MYSQL_ROOT_PASSWORD=root
MYSQL_USER=aluno
MYSQL_PASSWORD=aluno123
MYSQL_DATABASE=trabalho_ibd
MYSQL_PORT=3306

🐳 Subindo o Banco com Docker
1️⃣ Abra o Docker Desktop

Certifique-se de que ele está rodando antes de continuar.

2️⃣ No terminal, na pasta do projeto, execute:
docker-compose up -d


Esse comando:

Baixa a imagem do MySQL (se necessário)

Cria o container do banco

Carrega as variáveis do .env

Verificar Status
docker ps


Se aparecer algo como:

trabalho_ibd_mysql   Up   3306->3306


➡️ Tudo certo!

🧠 Populando o Banco com Python

Instale as dependências:

pip install -r requirements.txt


Execute o script:

python population_script.py


Isso irá:

Ler o arquivo .env

Conectar ao banco

Popular com dados sintéticos

🛠 Acessando via MySQL Workbench

Abra o MySQL Workbench → Clique em New Connection.

Configure usando os dados definidos no .env:

Campo	Valor
Host	localhost
Port	(verifique no .env — geralmente 3306 ou 3307)
User	aluno (ou definido no .env)
Password	A senha do .env
Database	trabalho_ibd (caso queira definir durante conexão)

Teste a conexão.
Se funcionar → salve.

Após esses passos, o banco estará:

✔ Criado
✔ Populado
✔ Disponível para consultas no MySQL Workbench

Agora você pode executar queries, verificar tabelas e trabalhar normalmente.
