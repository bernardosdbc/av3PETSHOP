import sys

# Não cria pastas __pycache__ dentro do projeto.
sys.dont_write_bytecode = True

from banco.inicializar import criar_tabelas
from servidor.servidor import iniciar

if "--inicializar" in sys.argv:
    criar_tabelas()
    print("Banco inicializado.")
else:
    try:
        iniciar()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
