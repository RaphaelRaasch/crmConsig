import datetime

EXPECTED_DICT_1040179875 = [
    {
        'contrato': '97-821163879/16',
        'matricula_id': '1040179875',
        'codigo_cartao': 76,
        'descricao_cartao': 'Reserva de Margem para Cartão de Crédito',
        'codigo_banco': '739',
        'nome_banco': 'BANCO CETELEM',
        'inicio_contrato': datetime.date(2016, 11, 9),
        'is_active': True,
        'inclusao_contrato': datetime.date(2016, 11, 9),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'limite_cartao': 1144.0,
        'valor_reservado': 44.0
    },
    {
        'contrato': '97-6298764/16',
        'matricula_id': '1040179875',
        'codigo_cartao': 71,
        'descricao_cartao': 'Reserva de Margem para Teste de Crédito',
        'codigo_banco': '43219',
        'nome_banco': 'BANCO Teste',
        'inicio_contrato': datetime.date(2019, 11, 9),
        'is_active': True,
        'inclusao_contrato': datetime.date(2011, 5, 9),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': True,
        'limite_cartao': 1244.0,
        'valor_reservado': 14.0
    },
    {
        'contrato': '97-4214513562/16',
        'matricula_id': '1040179875',
        'codigo_cartao': 79,
        'descricao_cartao': 'Reserva de Teste de Crédito',
        'codigo_banco': '31425',
        'nome_banco': 'BANCO CETELEM',
        'inicio_contrato': datetime.date(2030, 11, 9),
        'is_active': True,
        'inclusao_contrato': datetime.date(2010, 11, 9),
        'situacao': 'Desativado',
        'excluido_aps': True,
        'excluido_banco': True,
        'limite_cartao': 1148.0,
        'valor_reservado': 41.0
    },
]
