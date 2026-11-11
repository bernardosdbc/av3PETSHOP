from html import escape
from urllib.parse import quote

from banco import crud
from banco.opcoes import opcoes
from paginas.componentes import caixa_busca, seletor, sem_resultado

# Como cada tipo de campo aparece no formulário. Os outros tipos viram lista de escolha.
TIPOS_INPUT = {
    "text": 'type="text"',
    "date": 'type="date"',
    "time": 'type="time"',
    "number": 'type="number" step="0.01" min="0"',
}


def rotulo_da_coluna(cadastro, coluna):
    for nome, rotulo, tipo in cadastro.CAMPOS:
        if nome == coluna:
            return rotulo
    return coluna.upper()


def formulario(con, cadastro, atual, editar):
    html = '<form method="post" action="/' + cadastro.NOME + '" class="campos">'
    if atual:
        html += '<input type="hidden" name="_editar" value="' + escape(editar) + '">'

    for coluna, rotulo, tipo in cadastro.CAMPOS:
        valor = str(atual.get(coluna, cadastro.PADROES.get(coluna, "")))

        if tipo in TIPOS_INPUT:
            somente_leitura = ""
            if atual and coluna == cadastro.CHAVE:
                somente_leitura = " readonly"
            entrada = '<input name="' + coluna + '" value="' + escape(valor) + '" '
            entrada += TIPOS_INPUT[tipo] + " required" + somente_leitura + ">"
        else:
            entrada = seletor(coluna, opcoes(con, tipo), valor)

        html += "<label>" + rotulo + entrada + "</label>"

    html += '<div class="botoes"><button>Salvar</button>'
    if atual:
        html += '<a class="btn sec" href="/' + cadastro.NOME + '">Cancelar</a>'
    html += "</div></form>"
    return html


def tabela(cadastro, titulos, linhas, busca):
    if len(linhas) == 0:
        return sem_resultado(busca, "Nenhum registro ainda.")

    html = '<div class="rolagem"><table><tr>'
    for titulo in titulos:
        html += "<th>" + rotulo_da_coluna(cadastro, titulo) + "</th>"
    html += "<th></th></tr>"

    posicao_chave = titulos.index(cadastro.CHAVE)
    for linha in linhas:
        chave = str(linha[posicao_chave])
        html += "<tr>"
        for valor in linha:
            html += "<td>" + escape(str(valor)) + "</td>"

        html += '<td class="acoes">'
        html += '<a class="btn sec pequeno" href="/' + cadastro.NOME + "?editar=" + quote(chave) + '">Editar</a> '
        html += '<form method="post" action="/' + cadastro.NOME + '/excluir"'
        html += ' onsubmit="return confirm(\'Excluir este registro?\')">'
        html += '<input type="hidden" name="chave" value="' + escape(chave) + '">'
        html += '<button class="perigo pequeno">Excluir</button></form>'
        html += "</td></tr>"

    html += "</table></div>"
    return html


def montar(con, cadastro, editar, busca):
    titulos, linhas = crud.listar(con, cadastro, busca)

    atual = {}
    if editar:
        atual = crud.buscar_um(con, cadastro, editar)

    titulo_form = "Novo registro"
    if atual:
        titulo_form = "Editar registro"

    html = '<div class="cartao"><h2>' + titulo_form + "</h2>"
    html += formulario(con, cadastro, atual, editar) + "</div>"
    html += '<div class="cartao"><h2>' + cadastro.TITULO + "</h2>"
    html += caixa_busca(cadastro.NOME, cadastro.TITULO, busca)
    html += tabela(cadastro, titulos, linhas, busca) + "</div>"
    return html
