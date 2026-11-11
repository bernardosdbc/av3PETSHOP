from cadastros import agendamentos, animais, clientes, produtos, servicos

# O endereço da página (/clientes, /animais...) aponta para o cadastro certo.
CADASTROS = {
    "clientes": clientes,
    "animais": animais,
    "produtos": produtos,
    "servicos": servicos,
    "agendamentos": agendamentos,
}
