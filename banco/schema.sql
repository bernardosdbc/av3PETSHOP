CREATE TABLE IF NOT EXISTS clientes (
    id serial PRIMARY KEY,
    nome text NOT NULL,
    cpf text NOT NULL UNIQUE,
    telefone text NOT NULL,
    email text NOT NULL,
    endereco text NOT NULL
);

CREATE TABLE IF NOT EXISTS animais (
    id serial PRIMARY KEY,
    nome text NOT NULL,
    especie text NOT NULL,
    raca text NOT NULL,
    sexo text NOT NULL,
    data_nascimento date NOT NULL,
    cliente_id integer NOT NULL REFERENCES clientes (id)
);

CREATE TABLE IF NOT EXISTS produtos (
    codigo text PRIMARY KEY,
    nome text NOT NULL,
    descricao text NOT NULL,
    preco numeric(12, 2) NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS servicos (
    codigo text PRIMARY KEY,
    nome text NOT NULL,
    descricao text NOT NULL,
    preco numeric(12, 2) NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS vendas (
    id serial PRIMARY KEY,
    data date NOT NULL DEFAULT CURRENT_DATE,
    cliente_id integer NOT NULL REFERENCES clientes (id),
    total numeric(30, 2) NOT NULL CHECK (total >= 0)
);

CREATE TABLE IF NOT EXISTS itens_venda (
    venda_id integer NOT NULL REFERENCES vendas (id),
    produto_codigo text NOT NULL REFERENCES produtos (codigo),
    quantidade integer NOT NULL CHECK (quantidade > 0),
    preco_unitario numeric(12, 2) NOT NULL CHECK (preco_unitario >= 0),
    PRIMARY KEY (venda_id, produto_codigo)
);

CREATE TABLE IF NOT EXISTS agendamentos (
    id serial PRIMARY KEY,
    animal_id integer NOT NULL REFERENCES animais (id),
    servico_codigo text NOT NULL REFERENCES servicos (codigo),
    data date NOT NULL,
    horario time NOT NULL,
    status text NOT NULL DEFAULT 'agendado' CHECK (status IN ('agendado', 'realizado', 'cancelado'))
);
