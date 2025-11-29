# Trabalho Prático IBD - População de Banco de Dados

Este projeto implementa o ambiente de banco de dados e os scripts de geração de dados sintéticos.

## Configuração de Segurança (Importante)

Este projeto utiliza variáveis de ambiente para não expor senhas no código. Antes de rodar, siga os passos:

1. Localize o arquivo `.env.examplo`.
2. Faça uma cópia dele e renomeie para `.env`.
3. (Opcional) Edite o arquivo `.env` com as senhas que desejar.

## Passo 1: Subir o Banco de Dados

Com o arquivo `.env` criado, execute:

```docker-compose
docker-compose up -d
```

O Docker irá ler automaticamente as variáveis definidas no `.env`.

## Passo 2: Popular o Banco

O script Python também foi configurado para ler o mesmo arquivo `.env`.

```docker-compose
# Instale as dependências
pip install -r requirements.txt

# Execute o script
python population_script.py
```

## Estrutura do Projeto

* `docker-compose.yml`: Infraestrutura do banco.
* `population_script.py`: Script de população (lê configurações do .env).
* `BD_schema.sql`: Script DDL.
* `.env`: Arquivo de configuração local (Ignorado pelo Git).
