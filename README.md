# Projeto SQL

- Bruno Freitas de Nascimento Rodrigues
- Nicolas Byung Kwan Cho

---

## Como executar o projeto

1. Instalar as dependências dentro de requirements.txt

```
pip install -r requirements.txt
```

2. Dentro da raíz do projeto, criar o arquivo .env e incluir as variáveis de ambiente para acesso ao banco de dados:

```
USER = {nome do usuário}
PASSWORD = {senha do usuário}
DB = {nome do database}
```
3. Em seguida criar, no MySQL, o banco de dados com o mesmo nome utilizado

4. Para executar o aplicativo:

```
uvicorn sql_app.main:app --reload
```

As tabelas serão criadas automaticamente