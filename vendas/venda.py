from utilitarios.formato import padrao_busca


def listar(con, busca):
    sql = "SELECT v.id, v.data, c.nome, v.total FROM vendas v JOIN clientes c ON c.id = v.cliente_id"
    parametros = []

    if busca:
        # Procura no número da venda, no nome do cliente e nos produtos vendidos.
        sql += " WHERE v.id::text = %s OR c.nome ILIKE %s OR EXISTS ("
        sql += "SELECT 1 FROM itens_venda i JOIN produtos p ON p.codigo = i.produto_codigo "
        sql += "WHERE i.venda_id = v.id AND p.nome ILIKE %s)"
        parametros = [busca.lstrip("#"), padrao_busca(busca), padrao_busca(busca)]

    sql += " ORDER BY v.id DESC"
    return con.execute(sql, parametros).fetchall()


def listar_itens(con):
    sql = "SELECT i.venda_id, p.nome, i.quantidade, i.preco_unitario FROM itens_venda i "
    sql += "JOIN produtos p ON p.codigo = i.produto_codigo ORDER BY p.nome"
    return con.execute(sql).fetchall()


def listar_produtos(con):
    return con.execute("SELECT codigo, nome, preco FROM produtos ORDER BY nome").fetchall()


def registrar(con, cliente_id, produtos, quantidades):
    if cliente_id == "":
        raise ValueError("Escolha o cliente.")
    if len(produtos) == 0:
        raise ValueError("Adicione pelo menos um produto.")
    if len(produtos) != len(quantidades):
        raise ValueError("Informe o produto e a quantidade de cada item.")

    # Se o mesmo produto aparecer duas vezes, soma as quantidades.
    itens = {}
    posicao = 0
    for codigo in produtos:
        quantidade = int(quantidades[posicao])
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        itens[codigo] = itens.get(codigo, 0) + quantidade
        posicao += 1

    # Se algo falhar daqui para baixo, a conexão desfaz a venda inteira.
    resultado = con.execute(
        "INSERT INTO vendas (cliente_id, total) VALUES (%s, 0) RETURNING id", (cliente_id,)
    )
    venda_id = resultado.fetchone()[0]

    total = 0
    for codigo in itens:
        quantidade = itens[codigo]
        produto = con.execute("SELECT preco FROM produtos WHERE codigo = %s", (codigo,)).fetchone()
        if produto is None:
            raise ValueError("Produto " + codigo + " não encontrado.")
        preco = produto[0]
        con.execute(
            "INSERT INTO itens_venda (venda_id, produto_codigo, quantidade, preco_unitario) "
            "VALUES (%s, %s, %s, %s)",
            (venda_id, codigo, quantidade, preco),
        )
        total += preco * quantidade

    con.execute("UPDATE vendas SET total = %s WHERE id = %s", (total, venda_id))
