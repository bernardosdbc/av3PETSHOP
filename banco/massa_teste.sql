-- Massa de teste. Rode uma vez, com as tabelas já criadas:
--   psql -1 -v ON_ERROR_STOP=1 petshop -f massa_teste.sql
-- Se rodar de novo, o CPF repetido faz tudo ser desfeito (nada é duplicado).

INSERT INTO clientes (nome, cpf, telefone, email, endereco) VALUES
    ('Ana Souza',    '11111111111', '(11) 99999-1111', 'ana@email.com',    'Rua das Flores, 100'),
    ('Bruno Lima',   '22222222222', '(11) 98888-2222', 'bruno@email.com',  'Av. Brasil, 250'),
    ('Carla Mendes', '33333333333', '(11) 97777-3333', 'carla@email.com',  'Rua do Sol, 45');
-- Carla não tem animais nem vendas: dá para testar a exclusão dela.

INSERT INTO animais (nome, especie, raca, sexo, data_nascimento, cliente_id) VALUES
    ('Rex',   'Cachorro', 'Labrador',   'Macho', '2019-03-10', (SELECT id FROM clientes WHERE cpf = '11111111111')),
    ('Mel',   'Gato',     'Siamês',     'Fêmea', '2021-07-22', (SELECT id FROM clientes WHERE cpf = '11111111111')),
    ('Thor',  'Cachorro', 'Bulldog',    'Macho', '2020-11-05', (SELECT id FROM clientes WHERE cpf = '22222222222'));

INSERT INTO produtos (codigo, nome, descricao, preco) VALUES
    ('RACAO01', 'Ração Premium 10kg', 'Ração para cães adultos',   189.90),
    ('RACAO02', 'Ração Gatos 3kg',    'Ração para gatos castrados', 79.50),
    ('OSSO01',  'Osso de Couro',      'Osso para roer, pacote c/ 3', 12.00),
    ('COLEIRA', 'Coleira Ajustável',  'Coleira de nylon, tamanho M', 34.90),
    ('SHAMPOO', 'Shampoo Neutro',     'Shampoo para pele sensível 500ml', 27.75);

INSERT INTO servicos (codigo, nome, descricao, preco) VALUES
    ('BANHO',   'Banho',            'Banho completo com secagem',  60.00),
    ('TOSA',    'Tosa Higiênica',   'Tosa nas áreas de higiene',   45.00),
    ('CONSULTA','Consulta Veterinária', 'Consulta clínica geral', 150.00);

-- Venda 1 (Ana): 2x Ração Premium + 3x Osso = 415,80
INSERT INTO vendas (cliente_id, total) VALUES
    ((SELECT id FROM clientes WHERE cpf = '11111111111'), 415.80);
INSERT INTO itens_venda (venda_id, produto_codigo, quantidade, preco_unitario) VALUES
    ((SELECT max(id) FROM vendas), 'RACAO01', 2, 189.90),
    ((SELECT max(id) FROM vendas), 'OSSO01',  3,  12.00);

-- Venda 2 (Bruno): 1x Coleira + 2x Shampoo = 90,40
INSERT INTO vendas (cliente_id, total) VALUES
    ((SELECT id FROM clientes WHERE cpf = '22222222222'), 90.40);
INSERT INTO itens_venda (venda_id, produto_codigo, quantidade, preco_unitario) VALUES
    ((SELECT max(id) FROM vendas), 'COLEIRA', 1, 34.90),
    ((SELECT max(id) FROM vendas), 'SHAMPOO', 2, 27.75);

-- Um agendamento em cada status
INSERT INTO agendamentos (animal_id, servico_codigo, data, horario, status) VALUES
    ((SELECT id FROM animais WHERE nome = 'Rex'),  'BANHO',    CURRENT_DATE + 2, '09:00', 'agendado'),
    ((SELECT id FROM animais WHERE nome = 'Mel'),  'CONSULTA', CURRENT_DATE - 3, '14:30', 'realizado'),
    ((SELECT id FROM animais WHERE nome = 'Thor'), 'TOSA',     CURRENT_DATE + 5, '16:00', 'cancelado');
