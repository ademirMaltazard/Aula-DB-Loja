import mysql.connector

conexao = mysql.connector.connect(
    host='localhost', #onde está o meu banco
    user='root', #Usuário - root(super usuário)
    password='', #senha do usuario
    database='loja' #nome do banco
)

cursor = conexao.cursor()
print('Conectado com sucesso ao banco LOJA')


# Só pra ficar bonito kskksksk
def Linha():
    print('-' * 63)

def MostrarTitulo(titulo):
    Linha()
    print(f'{titulo:-^63}')
    Linha()

def Notificacao(msg):
    print(f'{msg:+^63}')

def Dado_formatado(dado):
    return print(f'| {dado[0]:>3} | {(dado[1]):<40} | R$ {(dado[2]):>7.2f} |')

#Aqui onde vai o CRUD
# C -> CREATE: INSERT
def InserirProduto():
    MostrarTitulo(' CADASTRAR NOVO PRODUTO ')
    novoProduto = input('Qual o nome do novo produto: ')
    # TENTA PROCURAR NO BANCO DE DADOS SE EXISTE ALGUM PRODUTO COM O MESMO NOME
    produto = ProcurarPorNome(novoProduto)
    if produto.__len__() > 0:
        # SE EXISTIR EXIBE A MENSAGEM E RETORNA
        print('já existe um produto com o nome digitado.\n'
              'Deseja EDITAR ou RETORNAR?')
        opcao = input('OPCAO 1 - EDITAR\n'
                      'PRECIONE ENTER PARA RETORNAR\n')
        if opcao == '1':
            AtualizarPorID(produto[0][0], produto[0]) # corta o vetor retornado em PRODUTO pra obter somente o ID e chama a funcao atualizar
            return
        else:
            # se voce digitar algo diferente de 1 ele retorna pro menu anterior
            return
    else:
        # SE NÃO EXISTIR CONTINUA A EXECUÇÃO DA FUNÇÃO
        novoPreco = float(input(f'Qual o preço do {novoProduto}: '))
        # nesse momento ja obtive os dados de NOME e  PRECO  e adiciono o produto no banco
        query = f"INSERT INTO produto (nome_produto, preco_produto)"\
                f"VALUES ('{novoProduto}',{novoPreco})"
        cursor.execute(query)
        # Aqui é onde vamos inserir os dados na tabala
        conexao.commit()
        # função minha pra exibir notificacao personalizada
        Notificacao(' Produto cadastrado com sucesso! ')
        print(f'| {(novoProduto):<30} | {(novoPreco):>7.2f} |')

#R - READ
def ExibirDados():
    MostrarTitulo(' PRODUTOS CADASTRADOS ')
    query = 'SELECT * FROM produto'
    cursor.execute(query)
    result = cursor.fetchall()
    if result.__len__() <= 0:
        Notificacao(' Nenhum produto cadastrado ')
    else:
        for indice in result:
            Dado_formatado(indice)
    Linha()

def ProcurarPorID(id):
    query = f'SELECT * FROM produto WHERE id_produto={id}'
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def ProcurarPorNome(nome):
    query = f'SELECT * FROM produto WHERE nome_produto="{nome}"'
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#U - UPDATE
def AtualizarPorID(id, produto):
    # LOOP DE VERIFICAÇÃO PARA EDIÇÃO DE DADOS
    while True:
        # COLETA DE QUAL CAMPO ELE DESEJA ALTERAR
        Notificacao(' Produto  a ser atualizado ')
        Dado_formatado(produto)
        Linha()
        print('Qual informação do produto você deseja alterar:')
        print(f'OPCAO 1 - NOME DO PRODUTO\n'
              f'OPCAO 2 - PREÇO DO PRODUTO\n'
              f'PRESSIONE SOMENTE *ENTER* PARA RETORNAR AO MENU PRINCIPAL\n')
        opcao = input('Selecione a opcao desejada: ')

        #
        if opcao == '1':
            alteracao = 'nome_produto'
            novo_dado = input('Qual o novo nome do produto: ')
        elif opcao == '2':
            alteracao = 'preco_produto'
            novo_dado = float(input('Qual o novo preco do produto: '))
        else:
            break


        confirm = input('Você confirma as alterações? Y/N : ').upper()

        if confirm == 'Y':
            query = f'UPDATE produto SET {alteracao} = "{novo_dado}" WHERE (id_produto = {id})'
            cursor.execute(query)
            conexao.commit()
            ProcurarPorID(id)
            break
        elif confirm == 'N':
            opcao = input(f'Deseja:\n'
                          f'OPCAO 1 - PREECHER NOVAMENTE\n'
                          f'PRESSIONE SOMENTE *ENTER* PARA RETORNAR AO MENU PRINCIPAL\n')
            if opcao == '1':
                print('Redirecionando...')
            elif opcao == '0':
                break
        else:
            print('OPÇÃO INVALIDA!!!')

#D - DELETE
def DeletarPorID(id, produto):
    Notificacao(' Produto  a ser DELETADO ')
    Dado_formatado(produto)
    Linha()
    opcao = input('Tem certeza que deseja apagar esse produto? Y/N\n').upper()
    if opcao == 'Y':
        query = f'DELETE FROM produto WHERE id_produto={id}'
        cursor.execute(query)
        conexao.commit()
        print('o produto foi deletado com sucesso')
    else:
        return Notificacao(' Operação cancelada, retornando...')


#------------------------- FUNÇÕES PARA MANIPULAÇÃO DE DADOS ----------------------------------------------------
def BuscarProduto():
    id = int(input('Qual a id do produto: '))
    # VERIFICANDO SE O PRODUTO EXISTE NO BANCO DE DADOS
    produto = ProcurarPorID(id)
    if produto.__len__() <= 0:
        # SE NÃO EXISTIR EXIBE A MENSAGEM E RETORNA
        Notificacao(' ID NÃO ENCONTRADA ')
    else:
        # SE EXISTIR CHAMA A FUNÇÃO
        Notificacao(' PRODUTO ENCONTRADO ')
        # Aqui mostramos o resultado da fução que vem como um VETOR de TUPLAS, PEGAMOS SÓ O PRIMEIRO RESULTADO
        Dado_formatado(ProcurarPorID(id)[0])

def DeletarProduto():
    MostrarTitulo(' EXCLUIR PRODUTO ')
    id = int(input('Qual a id do produto: '))
    # VERIFICANDO SE O PRODUTO EXISTE NO BANCO DE DADOS
    produto = ProcurarPorID(id)
    if produto.__len__() <= 0:
        # SE NÃO EXISTIR EXIBE A MENSAGEM E RETORNA
        Notificacao(' ID NÃO ENCONTRADA ')
    else:
        # SE EXISTIR CHAMA A FUNÇÃO
        DeletarPorID(id, produto[0])

def AtualizarProduto():
    MostrarTitulo(' ATUALIZAR PRODUTO ')
    id = int(input('Qual a id do produto: '))
    produto = ProcurarPorID(id)
    if produto.__len__() <= 0:
        # SE NÃO EXISTIR EXIBE A MENSAGEM E RETORNA
        Notificacao(' ID NÃO ENCONTRADA ')
    else:
        # SE EXISTIR CHAMA A FUNÇÃO
        AtualizarPorID(id, produto[0])

#-------------------------- PROTOTIPO FRONTEND -------------------------------------------------------
# INICIO DE LOOP DA APLICAÇÃO
while True:
    # MOSTRAR MENU DE OPÇÕES
    MostrarTitulo(' MENU ')
    print(f'OPCAO 1 - INSERIR NOVO PRODUTO\n'
          f'OPCAO 2 - MOSTRAR TODOS OS PRODUTOS\n'
          f'OPCAO 3 - BUSCAR POR ID\n'
          f'OPCAO 4 - DELETAR POR ID\n'
          f'OPCAO 5 - ATUALIZAR POR ID\n'
          f'OPCAO 0 - SAIR')
    opcao = input('Digite a opcao desejada: ')
    print()

    # INSERIR NOVO PRODUTO
    if opcao == '1':
        InserirProduto()

    # EXIBIR TODOS OS PRODUTOS
    elif opcao == '2':
        ExibirDados()

    # EXIBIR UM PRODUTO
    elif opcao == '3':
        BuscarProduto()

    # DELETAR O PRODUTO BUSCADO PELA ID
    elif opcao == '4':
        DeletarProduto()

    # ATUALIZAR INFORMAÇÕES DO PRODUTO BUSCANDO PELA ID
    elif opcao == '5':
        AtualizarProduto()

    # OPÇÃO PARA FECHAR A APLICAÇÃO
    elif opcao == '0':
        # Exibe a mensagem e encerra o programa
        print('Desenvolvido por Ademir MK. \nObrigado por ultilizar minha aplicação!!!')
        break

    else:
        Notificacao(' OPÇÃO INVALIDA!!! ')

    input('\nPRECIONE ENTER PARA CONTINUAR...\n')
