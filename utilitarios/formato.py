def dinheiro(valor):
    # 1250.5 vira "R$ 1.250,50"
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")
    return "R$ " + texto


def padrao_busca(busca):
    # Monta o texto do ILIKE. Os caracteres \, % e _ valem como texto comum.
    busca = busca.replace("\\", "\\\\")
    busca = busca.replace("%", "\\%")
    busca = busca.replace("_", "\\_")
    return "%" + busca + "%"
