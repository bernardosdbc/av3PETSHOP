from utilitarios.formato import padrao_busca

# Funções de banco usadas por todos os cadastros (clientes, animais, produtos...).
# Cada cadastro informa TABELA, CHAVE e CAMPOS. Os nomes vêm do nosso código, nunca do usuário.


def colunas_do_formulario(cadastro):
    colunas = []
    for coluna, rotulo, tipo in cadastro.CAMPOS:
        colunas.append(coluna)
    return colunas


def listar(con, cadastro, busca):
    sql = "SELECT * FROM " + cadastro.TABELA
    parametros = []

    if busca:
        colunas = colunas_do_formulario(cadastro)
        if cadastro.CHAVE not in colunas:
            colunas.insert(0, cadastro.CHAVE)
        partes = []
        for coluna in colunas:
            partes.append(coluna + "::text")
        sql += " WHERE (" + " || ' ' || ".join(partes) + ") ILIKE %s"
        parametros.append(padrao_busca(busca))

    sql += " ORDER BY " + cadastro.CHAVE
    resultado = con.execute(sql, parametros)

    titulos = []
    for coluna in resultado.description:
        titulos.append(coluna.name)
    return titulos, resultado.fetchall()


def buscar_um(con, cadastro, chave):
    sql = "SELECT * FROM " + cadastro.TABELA + " WHERE " + cadastro.CHAVE + " = %s"
    resultado = con.execute(sql, (chave,))
    linha = resultado.fetchone()
    if linha is None:
        return {}

    registro = {}
    posicao = 0
    for coluna in resultado.description:
        registro[coluna.name] = linha[posicao]
        posicao += 1
    return registro


def inserir(con, cadastro, form):
    colunas = colunas_do_formulario(cadastro)
    valores = []
    for coluna in colunas:
        valores.append(form.get(coluna, ""))

    espacos = ", ".join(["%s"] * len(colunas))
    sql = "INSERT INTO " + cadastro.TABELA + " (" + ", ".join(colunas) + ") VALUES (" + espacos + ")"
    con.execute(sql, valores)


def atualizar(con, cadastro, chave, form):
    atribuicoes = []
    valores = []
    for coluna in colunas_do_formulario(cadastro):
        if coluna != cadastro.CHAVE:
            atribuicoes.append(coluna + " = %s")
            valores.append(form.get(coluna, ""))
    valores.append(chave)

    sql = "UPDATE " + cadastro.TABELA + " SET " + ", ".join(atribuicoes)
    sql += " WHERE " + cadastro.CHAVE + " = %s"
    con.execute(sql, valores)


def excluir(con, cadastro, chave):
    sql = "DELETE FROM " + cadastro.TABELA + " WHERE " + cadastro.CHAVE + " = %s"
    con.execute(sql, (chave,))
