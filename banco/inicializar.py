import os

from banco.conexao import conectar


def criar_tabelas():
    caminho = os.path.join(os.path.dirname(__file__), "schema.sql")
    arquivo = open(caminho, encoding="utf-8")
    sql = arquivo.read()
    arquivo.close()

    with conectar() as con:
        con.execute(sql)
