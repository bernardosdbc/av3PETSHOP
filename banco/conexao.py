import os

import psycopg

# Para usar outro banco, defina a variável PETSHOP_DATABASE_URL.
BANCO = os.getenv("PETSHOP_DATABASE_URL", "dbname=petshop")


def conectar():
    return psycopg.connect(BANCO)
