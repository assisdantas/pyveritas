# Blockchain com Flask e Autenticação
Este projeto implementa um blockchain simples usando o framework Flask e um sistema de autenticação baseado em tokens JWT. O projeto também inclui a mineração de blocos, armazenamento no banco de dados PostgreSQL e criptografia de senhas com bcrypt.

## Funcionalidades
- **Mineração de Blocos**: Permite adicionar blocos à blockchain através de transações.
- **Autenticação de Usuários**: Suporte para registro, login e verificação de tokens JWT para autenticação.
- **Armazenamento Persistente**: Todos os blocos e tokens de autenticação são armazenados em um banco de dados PostgreSQL.
- **Criptografia de Senhas**: Senhas são armazenadas de forma segura utilizando bcrypt.

## Requisitos
Antes de rodar o projeto, você precisa instalar algumas dependências. Para isso, você pode usar o pipenv para criar e gerenciar um ambiente virtual com as dependências necessárias.

1. Python 3.8+
1. PostgreSQL: Você precisa de um banco de dados PostgreSQL configurado.

## Instalação das Dependências
Instale as dependências do projeto com o pipenv:

```bash
pipenv install
```

Ou, se não estiver usando o pipenv, instale as dependências diretamente com o pip:

```bash
pip install -r requirements.txt
```

## Configuração do Ambiente
Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:

```
DB_NAME=seu_nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=sua_chave_secreta
```

## Estrutura do Projeto
A estrutura do projeto é organizada da seguinte forma:

```
/pyveritas
|-- app/
|   |-- __init__.py
|   |-- blockchain.py
|   |-- block.py
|   |-- transaction.py
|   |-- consensus.py
|-- server/
|   |-- __init__.py
|   |-- app.py
|   |-- auth.py
|-- db/
|   |-- __init__.py
|   |-- database.py
|-- config.py
|-- requirements.txt
|-- run.py
```
## Como Rodar o Projeto
### Configuração do Banco de Dados:

Certifique-se de que o PostgreSQL está em execução e configure um banco de dados com as tabelas apropriadas. O script já faz a execução dos mesmos comandos abaixo, ou seja, se as tabelas não existirem, ele criará.

# Rodando a Aplicação:

Após configurar o banco de dados e o arquivo .env, você pode rodar o servidor Flask com o seguinte comando:

```bash
python app.py
```

A aplicação estará disponível em http://localhost:5000.

## Endpoints

#### 1. Login
Autentica um usuário e retorna um token JWT válido.

Rota: `/login`
Método: `POST`

Dados:

```json
{
  "username": "seu_username",
  "password": "sua_senha"
}
```

Resposta:

```json
{
  "token": "seu_token_aqui"
}
```

#### 2. Registro de Usuário
Registra um novo usuário no sistema com um nome de usuário e senha.

Rota: `/register`
Método: `POST`

Dados:

```json
{
  "username": "novo_username",
  "password": "nova_senha"
}
```

Resposta:

```json
{
  "message": "User registered successfully."
}
```

#### 3. Minerar Bloco
Minerar um novo bloco e adicionar à blockchain.

Rota:` /mine_block`
Método:` POST`
Cabeçalhos:

```
Authorization: Bearer <token>
```

Dados:

```json
{
  "transactions": "Transação 1, Transação 2"
}
```

Resposta:

```json
{
  "message": "Block mined successfully.",
  "block": 1
}
```

#### 4. Obter a Blockchain
Retorna todos os blocos da blockchain.

Rota:` /get_chain`
Método: `GET`

Resposta:

```json
[
  {
    "index": 1,
    "previous_hash": "0000",
    "timestamp": "2024-11-13 10:00:00",
    "transactions": "Transação 1",
    "hash": "abc123",
    "nonce": 12345
  },
]
```

## Segurança
- **Criptografia de Senhas**: As senhas são armazenadas de forma segura usando bcrypt.
- **Tokens JWT**: São gerados e verificados para autenticação e autorização de usuários.

## Funcionalidades de Autenticação
- Criação de Token: Ao fazer login, o usuário recebe um token JWT.
- Verificação de Token: O token é verificado em todas as rotas protegidas.

## Contribuindo
1. Faça um fork deste repositório.
2. Crie uma branch para sua modificação
```bash
git checkout -b feature/nova-funcionalidade
```
3. Faça commit das suas mudanças
```bash
git commit -am 'Adicionando nova funcionalidade'
```
4. Envie para o repositório remoto
```bash
git push origin feature/nova-funcionalidade
```
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.
