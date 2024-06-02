import sqlite3 as lite

con = lite.connect('dados.db')

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