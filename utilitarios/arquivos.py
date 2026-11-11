import os


def ler_arquivo(pasta, nome):
    # Lê um arquivo de texto que fica na mesma pasta de quem chamou (passe __file__).
    caminho = os.path.join(os.path.dirname(pasta), nome)
    arquivo = open(caminho, encoding="utf-8")
    texto = arquivo.read()
    arquivo.close()
    return texto
