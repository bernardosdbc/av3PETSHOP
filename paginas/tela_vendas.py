from html import escape

from banco.opcoes import opcoes
from paginas.componentes import caixa_busca, seletor, sem_resultado
from utilitarios.arquivos import ler_arquivo
from utilitarios.formato import dinheiro
from vendas import venda

CARRINHO = ler_arquivo(__file__, "carrinho.js")


def formulario_venda(con, produtos):
    clientes = opcoes(con, "cliente")

    if len(produtos) == 0 or len(clientes) == 0:
        html = '<div class="cartao"><h2>Nova venda</h2><p class="vazio">Para vender, cadastre antes '
        html += 'pelo menos um <a href="/clientes">cliente</a> e um <a href="/produtos">produto</a>.</p></div>'
        return html

    escolhas_produto = ""
    for codigo, nome, preco in produtos:
        escolhas_produto += '<option value="' + escape(codigo) + '" data-preco="' + str(preco) + '">'
        escolhas_produto += escape(nome) + " — " + dinheiro(preco) + "</option>"

    # Lado esquerdo: itens do carrinho. Lado direito: cliente, total e botão.
    html = '<form method="post" action="/vendas" id="venda" class="venda-layout">'
    html += '<div class="cartao"><h2>Itens da venda</h2><div id="itens"></div>'
    html += '<button type="button" id="adicionar" class="mais">+ Adicionar produto</button></div>'
    html += '<div class="cartao resumo-venda"><h2>Resumo</h2>'
    html += "<label>Cliente" + seletor("cliente_id", clientes) + "</label>"
    html += '<div><span class="suave"><span id="unidades">0</span> unidade(s)</span>'
    html += '<div class="valor-total" id="total">R$ 0,00</div></div>'
    html += '<button class="grande">Finalizar venda</button></div></form>'

    # Modelo de uma linha do carrinho. O JavaScript copia este modelo a cada "Adicionar produto".
    html += '<template id="modelo"><div class="item-venda">'
    html += '<select name="produto" required><option value="">Selecione o produto…</option>'
    html += escolhas_produto + "</select>"
    html += '<div class="qtd"><button type="button" data-passo="-1">−</button>'
    html += '<input name="quantidade" type="number" min="1" value="1">'
    html += '<button type="button" data-passo="1">+</button></div>'
    html += '<b class="sub">—</b>'
    html += '<button type="button" class="remover" title="Remover item">×</button></div></template>'
    html += "<script>" + CARRINHO + "</script>"
    return html


def historico(con, busca):
    vendas = venda.listar(con, busca)

    # Junta os itens de cada venda: {numero_da_venda: "html dos itens"}
    itens_por_venda = {}
    for venda_id, nome, quantidade, preco in venda.listar_itens(con):
        texto = "<div>" + str(quantidade) + "× " + escape(nome)
        texto += ' <span class="suave">' + dinheiro(preco) + " cada</span></div>"
        itens_por_venda[venda_id] = itens_por_venda.get(venda_id, "") + texto

    if len(vendas) == 0:
        return sem_resultado(busca, "Nenhuma venda registrada ainda.")

    html = '<div class="rolagem"><table><tr><th>Venda</th><th>Data</th><th>Cliente</th>'
    html += "<th>Itens</th><th>Total</th></tr>"
    for venda_id, data, cliente, total in vendas:
        html += "<tr><td>#" + str(venda_id) + "</td>"
        html += "<td>" + data.strftime("%d/%m/%Y") + "</td>"
        html += "<td>" + escape(cliente) + "</td>"
        html += "<td>" + itens_por_venda.get(venda_id, "") + "</td>"
        html += "<td><b>" + dinheiro(total) + "</b></td></tr>"
    html += "</table></div>"
    return html


def montar(con, busca):
    html = formulario_venda(con, venda.listar_produtos(con))
    html += '<div class="cartao" style="margin-top:20px"><h2>Histórico de vendas</h2>'
    html += caixa_busca("vendas", "Vendas", busca)
    html += historico(con, busca) + "</div>"
    return html
