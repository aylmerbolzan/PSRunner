import sqlite3 as lite

con = lite.connect('../data/dados.db')

# CREATE - Comando
def inserir_comando(i):
    with con:
        cur = con.cursor()
        query = ("INSERT INTO comandos(nome, descricao, codigo) VALUES(?, ?, ?)")
        cur.execute(query, i)

# READ - Comando
def ver_comandos():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM comandos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

# DELETE - Comando
def deletar_comando(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM comandos WHERE id = ?"
        cur.execute(query, (i)) 

# Ver dados da tabela
def montar_grid():
    comandos = ver_comandos()
    lista_tabela = []

    for i in comandos:
        lista_tabela.append(i)

    return lista_tabela

def atualizar_comando(comando):
    id_comando = comando[-1]
    comando.pop()

    with con:
        cur = con.cursor()
        query = "UPDATE comandos SET nome = ?, descricao = ?, codigo = ? WHERE id = ?"
        cur.execute(query, (*comando, id_comando))