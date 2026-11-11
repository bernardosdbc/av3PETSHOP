STATUS = ["agendado", "realizado", "cancelado"]


def opcoes(con, tipo):
    # Devolve a lista de (valor, texto) usada nos campos de escolha dos formulários.
    resultado = []

    if tipo == "status":
        for status in STATUS:
            resultado.append((status, status.capitalize()))
        return resultado

    if tipo == "cliente":
        linhas = con.execute("SELECT id, nome FROM clientes ORDER BY nome").fetchall()
    elif tipo == "animal":
        linhas = con.execute("SELECT id, nome FROM animais ORDER BY nome").fetchall()
    else:
        linhas = con.execute("SELECT codigo, nome FROM servicos ORDER BY nome").fetchall()

    for valor, nome in linhas:
        resultado.append((str(valor), nome + " (#" + str(valor) + ")"))
    return resultado
