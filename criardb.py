import sqlite3 as lite

con = lite.connect('dados.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE comandos(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, descricao TEXT, codigo TEXT)")