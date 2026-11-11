from html import escape


def seletor(nome, escolhas, atual="", obrigatorio=True):
    # Lista de escolha (<select>). escolhas é uma lista de (valor, texto).
    exigir = ""
    if obrigatorio:
        exigir = " required"

    html = '<select name="' + nome + '"' + exigir + '><option value="">Selecione…</option>'
    for valor, texto in escolhas:
        marcado = ""
        if valor == atual:
            marcado = " selected"
        html += '<option value="' + escape(valor) + '"' + marcado + ">" + escape(texto) + "</option>"
    html += "</select>"
    return html


def caixa_busca(endereco, titulo, busca):
    limpar = ""
    if busca:
        limpar = '<a class="btn sec" href="/' + endereco + '">Limpar</a>'

    html = '<form method="get" action="/' + endereco + '" class="busca">'
    html += '<input type="search" name="busca" value="' + escape(busca) + '"'
    html += ' placeholder="Buscar em ' + titulo.lower() + '…">'
    html += "<button>Buscar</button>" + limpar + "</form>"
    return html


def sem_resultado(busca, texto_vazio):
    if busca:
        return '<p class="vazio">Nada encontrado para “' + escape(busca) + '”.</p>'
    return '<p class="vazio">' + texto_vazio + "</p>"
