# niponcred api

API da aplicação niponcred

## Requisitos do sistema

* MySQL 5.7+
* Python 3

## Desenvolvimento

### Iniciando o virtualenv

```
virtualenv -p /usr/bin/python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Para rodar a API

Apontar para `run.py`

```
APP_WEB_URL=http://localhost:8282/#!
SENDGRID_API_KEY=TESTE
DATABASE_URL=mysql+pymysql://niponcred:niponcred@localhost/niponcred?charset=utf8mb4
```

## Banco de dados local

1. Criar o schema **niponcred** usando o character set **utf8mb4** e o collation **utf8mb4_unicode_ci**
2. Criar o usuário **niponcred** com a senha **niponcred**
3. Dar todas permissões para o usuário **niponcred** no schema **niponcred**
4. Ou rodar os comando abaixo:

```bash
mysql -u root -p
CREATE USER 'niponcred'@'%' IDENTIFIED BY 'v';
CREATE SCHEMA `niponcred` DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
GRANT ALL ON `niponcred`.* TO 'niponcred'@'%';
```

## Usando o Alembic (Alterações no banco)

### Criando uma novas revisão

``` bash
alembic revision -m 'Indique aqui uma descrição para revisão'
```

### Atualizando o banco

```bash
alembic upgrade head
```

### Atualizando o banco e incluindo massa de dados

```bash
alembic -x data=true upgrade head
```

### Release Version (Production)

1. Criar uma nova release usando o [git-flow](http://danielkummer.github.io/git-flow-cheatsheet/)
1. Atualizar `APP_VERSION` e `ALEMBIC_VERSION` no arquivo `config.py`
1. Atualizar `VERSION` no arquivo `fabfile.py`
1. Comitar as alterações referenciando a release a ser criada.
1. Finalizar a release

### Cabeçalhos

```
Content-Type: application/json
Authentication-Token: <token de autenticação>
```

### Mais informações

A API é criada usando o **Flask-Restless**

* [Formato das requisições e das respostas](https://flask-restless.readthedocs.io/en/0.17.0/requestformat.html)
* [Formato das pesquisas](https://flask-restless.readthedocs.io/en/0.17.0/searchformat.html#quick-examples)