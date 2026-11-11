from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse

import psycopg

from banco.conexao import conectar
from cadastros.todos import CADASTROS
from paginas import tela_cadastro, tela_vendas
from paginas.layout import pagina
from servidor.acoes import processar

PORTA = 8000


def primeiro_valor(consulta, nome):
    valores = consulta.get(nome, [""])
    return valores[0]


def endereco_existe(nome):
    return nome == "vendas" or nome in CADASTROS


class Servidor(BaseHTTPRequestHandler):
    def responder(self, status, html):
        corpo = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        url = urlparse(self.path)
        nome = url.path.strip("/")
        if nome == "":
            nome = "clientes"

        if not endereco_existe(nome):
            self.responder(404, pagina("<p>Página não encontrada.</p>"))
            return

        consulta = parse_qs(url.query)
        busca = primeiro_valor(consulta, "busca").strip()
        editar = primeiro_valor(consulta, "editar")
        erro = primeiro_valor(consulta, "erro")
        ok = primeiro_valor(consulta, "ok")

        try:
            with conectar() as con:
                if nome == "vendas":
                    corpo = tela_vendas.montar(con, busca)
                else:
                    corpo = tela_cadastro.montar(con, CADASTROS[nome], editar, busca)
            self.responder(200, pagina(corpo, nome, erro, ok))
        except psycopg.Error as e:
            mensagem = e.diag.message_primary or "Erro no banco de dados."
            self.responder(500, pagina("", nome, mensagem))

    def do_POST(self):
        partes = urlparse(self.path).path.strip("/").split("/")
        if not endereco_existe(partes[0]):
            self.responder(404, pagina("<p>Página não encontrada.</p>"))
            return

        tamanho = int(self.headers.get("Content-Length", 0))
        dados = self.rfile.read(tamanho).decode("utf-8")
        listas = parse_qs(dados)

        form = {}
        for campo in listas:
            form[campo] = listas[campo][0]

        erro = ""
        try:
            with conectar() as con:
                processar(con, partes, form, listas)
        except ValueError as e:
            erro = str(e)
        except psycopg.Error as e:
            erro = e.diag.message_primary or "Erro no banco de dados."

        # Depois de salvar, volta para a página (assim atualizar a tela não repete o envio).
        destino = "/" + partes[0] + "?"
        if erro:
            destino += "erro=" + quote(erro)
        else:
            destino += "ok=Salvo+com+sucesso."
        self.send_response(303)
        self.send_header("Location", destino)
        self.end_headers()


def iniciar():
    print("Pet Shop: http://127.0.0.1:" + str(PORTA))
    ThreadingHTTPServer(("127.0.0.1", PORTA), Servidor).serve_forever()
