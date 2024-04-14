import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='loja'
)

cursor = conexao.cursor()
print('conectado com sucesso!!!')

def CadastrarProduto():
    nameProduct = 'headset hyperX'
    price = 150.00

    query = f'INSERT INTO produto (nome_produto, preco_produto) VALUES ("{nameProduct}", {price})'
    cursor.execute(query)
    conexao.commit()

def BuscarTodos():
    query = f'SELECT * FROM produto'
    cursor.execute(query)
    produtos = cursor.fetchall()
    print(produtos)

def BuscarUmProduto():
    id = 2
    query = f'SELECT * FROM produto WHERE id_produto = {id}'
    cursor.execute(query)
    produto = cursor.fetchall()
    print(produto)

def atualizarProduto():
    id_produto = 2
    new_name = 'novo nome'
    new_price = 500.55

    query = f'UPDATE produto SET nome_produto = "{new_name}", preco_produto = {new_price} WHERE id_produto = {id_produto}'
    cursor.execute(query)
    conexao.commit()

def deletarProduto():
    id_produto = 2
    query = f'DELETE FROM produto WHERE id_produto = {id_produto}'
    cursor.execute(query)
    conexao.commit()

#CadastrarProduto()
#BuscarTodos()
BuscarUmProduto()