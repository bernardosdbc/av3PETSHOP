from html import escape

from utilitarios.arquivos import ler_arquivo

ESTILO = ler_arquivo(__file__, "estilo.css")

# (endereço, texto da aba)
MENU = [
    ("clientes", "Clientes"),
    ("animais", "Animais"),
    ("produtos", "Produtos"),
    ("servicos", "Serviços"),
    ("agendamentos", "Agenda"),
    ("vendas", "Vendas"),
]


def pagina(corpo, ativo="", erro="", ok=""):
    abas = ""
    for endereco, titulo in MENU:
        classe = ""
        if endereco == ativo:
            classe = ' class="ativo"'
        abas += '<a href="/' + endereco + '"' + classe + ">" + titulo + "</a>"

    avisos = ""
    if erro:
        avisos += '<div class="aviso erro">' + escape(erro) + "</div>"
    if ok:
        avisos += '<div class="aviso ok">' + escape(ok) + "</div>"

    html = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1">'
    html += "<title>Pet Shop</title><style>" + ESTILO + "</style></head><body>"
    html += "<header><h1>🐾 Pet Shop</h1><nav>" + abas + "</nav></header>"
    html += "<main>" + avisos + corpo + "</main></body></html>"
    return html
