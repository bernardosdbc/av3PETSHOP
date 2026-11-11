NOME = "agendamentos"
TITULO = "Agenda"
TABELA = "agendamentos"
CHAVE = "id"

CAMPOS = [
    ("animal_id", "Animal", "animal"),
    ("servico_codigo", "Serviço", "servico"),
    ("data", "Data", "date"),
    ("horario", "Horário", "time"),
    ("status", "Status", "status"),
]

# Valor que já vem preenchido no formulário de cadastro.
PADROES = {"status": "agendado"}


def validar(form):
    pass
