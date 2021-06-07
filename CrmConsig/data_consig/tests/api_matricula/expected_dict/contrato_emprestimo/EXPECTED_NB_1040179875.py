import datetime

today_day = datetime.date.today().day

EXPECTED_DICT_1040179875 = [
    {
        'contrato': '603206964',
        'matricula_id': '1040179875',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '029',
        'nome_banco': 'ITAU CONSIGNADO',
        'data_inicio': datetime.date(2019, 11, 1),
        'competencia_inicio_desconto': datetime.date(2020, 1, today_day),
        'competencia_fim_desconto': datetime.date(2025, 12, today_day),
        'data_inclusao': datetime.date(2019, 11, 13),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 2225.28,
        'valor_parcela': 49.14,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 71,
        'saldo': 2220.48,
        'taxa': 1.39
    },
    {
        'contrato': '22-838836069/19',
        'matricula_id': '1040179875',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '739',
        'nome_banco': 'BANCO CETELEM',
        'data_inicio': datetime.date(2019, 8, 1),
        'competencia_inicio_desconto': datetime.date(2019, 10, today_day),
        'competencia_fim_desconto': datetime.date(2025, 9, today_day)
        if today_day < 31 else datetime.date(2025, 9, today_day - 1),
        'data_inclusao': datetime.date(2019, 8, 15),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 3174.63,
        'valor_parcela': 77.0,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 68,
        'saldo': 3116.16,
        'taxa': 1.71
    },
    {
        'contrato': '326277882-6',
        'matricula_id': '1040179875',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '623',
        'nome_banco': 'PAN',
        'data_inicio': datetime.date(2019, 4, 3),
        'competencia_inicio_desconto': datetime.date(2019, 5, today_day),
        'competencia_fim_desconto': datetime.date(2025, 4, today_day)
        if today_day < 31 else datetime.date(2025, 4, today_day - 1),
        'data_inclusao': datetime.date(2019, 4, 3),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 663.03,
        'valor_parcela': 18.85,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 63,
        'saldo': 640.72,
        'taxa': 2.28
    },
    {
        'contrato': '210347110002789140',
        'matricula_id': '1040179875',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '104',
        'nome_banco': 'CAIXA',
        'data_inicio': datetime.date(2018, 12, 29),
        'competencia_inicio_desconto': datetime.date(2019, 2, today_day)
        if today_day < 31 else datetime.date(2019, 2, today_day - 2),
        'competencia_fim_desconto': datetime.date(2025, 1, today_day),
        'data_inclusao': datetime.date(2018, 12, 29),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 4150.0,
        'valor_parcela': 108.62,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 60,
        'saldo': 3867.67,
        'taxa': 1.98
    },
    {
        'contrato': '572528265',
        'matricula_id': '1040179875',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '029',
        'nome_banco': 'ITAU CONSIGNADO',
        'data_inicio': datetime.date(2017, 4, 11),
        'competencia_inicio_desconto': datetime.date(2017, 6, today_day)
        if today_day < 31 else datetime.date(2017, 6, today_day - 1),
        'competencia_fim_desconto': datetime.date(2023, 5, today_day),
        'data_inclusao': datetime.date(2017, 4, 11),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 605.86,
        'valor_parcela': 17.17,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 40,
        'saldo': 469.68,
        'taxa': 2.27
    },
    {
        'contrato': '000002073076',
        'matricula_id': '1040179875',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '422',
        'nome_banco': 'SAFRA',
        'data_inicio': datetime.date(2016, 7, 28),
        'competencia_inicio_desconto': datetime.date(2016, 9, today_day)
        if today_day < 31 else datetime.date(2016, 9, 30),
        'competencia_fim_desconto': datetime.date(2022, 8, today_day),
        'data_inclusao': datetime.date(2016, 7, 28),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 949.54,
        'valor_parcela': 28.62,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 31,
        'saldo': 666.42,
        'taxa': 2.51
    },
]
