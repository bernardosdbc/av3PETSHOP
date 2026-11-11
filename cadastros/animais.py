from datetime import date

NOME = "animais"
TITULO = "Animais"
TABELA = "animais"
CHAVE = "id"

CAMPOS = [
    ("nome", "Nome", "text"),
    ("especie", "Espécie", "text"),
    ("raca", "Raça", "text"),
    ("sexo", "Sexo", "text"),
    ("data_nascimento", "Data de nascimento", "date"),
    ("cliente_id", "Cliente", "cliente"),
]

PADROES = {}


def validar(form):
    nascimento = form.get("data_nascimento", "")
    if nascimento > date.today().isoformat():
        raise ValueError("A data de nascimento não pode ser futura.")
