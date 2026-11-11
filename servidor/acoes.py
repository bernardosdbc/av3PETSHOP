from banco import crud
from cadastros.todos import CADASTROS
from vendas import venda


def processar(con, partes, form, listas):
    # partes vem do endereço. Exemplos: ["clientes"] (salvar) ou ["clientes", "excluir"].
    # form tem o primeiro valor de cada campo; listas tem todos os valores (usado nos itens da venda).
    nome = partes[0]

    if nome == "vendas":
        venda.registrar(
            con,
            form.get("cliente_id", ""),
            listas.get("produto", []),
            listas.get("quantidade", []),
        )
        return

    cadastro = CADASTROS[nome]

    if partes[1:] == ["excluir"]:
        crud.excluir(con, cadastro, form.get("chave", ""))
    elif "_editar" in form:
        cadastro.validar(form)
        crud.atualizar(con, cadastro, form["_editar"], form)
    else:
        cadastro.validar(form)
        crud.inserir(con, cadastro, form)
