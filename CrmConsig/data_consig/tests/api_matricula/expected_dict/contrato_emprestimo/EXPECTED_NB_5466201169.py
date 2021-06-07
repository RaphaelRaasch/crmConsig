import datetime

today_day = datetime.date.today().day

EXPECTED_DICT_5466201169 = [
    {
        'contrato': '332335637-2',
        'matricula_id': '5466201169',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '623',
        'nome_banco': 'PAN',
        'data_inicio': datetime.date(2020, 1, 22),
        'competencia_inicio_desconto': datetime.date(2020, 2, today_day)
        if today_day < 31 else datetime.date(2020, 2, today_day - 2),
        'competencia_fim_desconto': datetime.date(2026, 1, today_day),
        'data_inclusao': datetime.date(2020, 1, 22),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 1530.75,
        'valor_parcela': 43.06,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 72,
        'saldo': 1557.07,
        'taxa': 2.24
    },
    {
        'contrato': '00000000000008009243',
        'matricula_id': '5466201169',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '041',
        'nome_banco': 'BANRISUL',
        'data_inicio': datetime.date(2020, 1, 5),
        'competencia_inicio_desconto': datetime.date(2020, 2, today_day)
        if today_day < 31 else datetime.date(2020, 2, today_day - 2),
        'competencia_fim_desconto': datetime.date(2025, 5, today_day),
        'data_inclusao': datetime.date(2020, 1, 5),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 5232.35,
        'valor_parcela': 123.16,
        'quantidade_parcelas': 64,
        'parcelas_aberto': 64,
        'saldo': 5253.4,
        'taxa': 1.37
    },
    {
        'contrato': '607100239',
        'matricula_id': '5466201169',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '029',
        'nome_banco': 'ITAU CONSIGNADO',
        'data_inicio': datetime.date(2019, 10, 22),
        'competencia_inicio_desconto': datetime.date(2019, 11, today_day)
        if today_day < 31 else datetime.date(2019, 11, today_day - 1),
        'competencia_fim_desconto': datetime.date(2025, 10, today_day),
        'data_inclusao': datetime.date(2019, 10, 22),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 6272.69,
        'valor_parcela': 176.2,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 70,
        'saldo': 6313.11,
        'taxa': 2.24
    },
    {
        'contrato': '927689324',
        'matricula_id': '5466201169',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '001',
        'nome_banco': 'BRASIL',
        'data_inicio': datetime.date(2019, 10, 8),
        'competencia_inicio_desconto': datetime.date(2019, 11, today_day)
        if today_day < 31 else datetime.date(2019, 11, today_day - 1),
        'competencia_fim_desconto': datetime.date(2025, 10, today_day),
        'data_inclusao': datetime.date(2019, 10, 8),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 46475.25,
        'valor_parcela': 994.59,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 70,
        'saldo': 45896.88,
        'taxa': 1.29
    },
    {
        'contrato': '0005416393',
        'matricula_id': '5466201169',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '935',
        'nome_banco': 'FACTA',
        'data_inicio': datetime.date(2019, 9, 4),
        'competencia_inicio_desconto': datetime.date(2019, 9, today_day)
        if today_day < 31 else datetime.date(2019, 9, today_day - 1),
        'competencia_fim_desconto': datetime.date(2025, 8, today_day),
        'data_inclusao': datetime.date(2019, 9, 4),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 6165.18,
        'valor_parcela': 133.67,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 68,
        'saldo': 5987.82,
        'taxa': 1.33
    },
    {
        'contrato': '161790066',
        'matricula_id': '5466201169',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '955',
        'nome_banco': 'OLE CONSIGNADO',
        'data_inicio': datetime.date(2019, 4, 13),
        'competencia_inicio_desconto': datetime.date(2019, 5, today_day),
        'competencia_fim_desconto': datetime.date(2025, 4, today_day)
        if today_day < 31 else datetime.date(2025, 4, today_day - 1),
        'data_inclusao': datetime.date(2019, 4, 13),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 526.1,
        'valor_parcela': 15.0,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 64,
        'saldo': 511.88,
        'taxa': 2.29
    },
    {
        'contrato': '594413681',
        'matricula_id': '5466201169',
        'codigo_emprestimo': 98,
        'descricao_emprestimo': 'Empréstimo por Consignação',
        'codigo_banco': '029',
        'nome_banco': 'ITAU CONSIGNADO',
        'data_inicio': datetime.date(2019, 2, 3),
        'competencia_inicio_desconto': datetime.date(2019, 2, today_day)
        if today_day < 31 else datetime.date(2019, 2, today_day - 2),
        'competencia_fim_desconto': datetime.date(2025, 1, today_day),
        'data_inclusao': datetime.date(2019, 2, 3),
        'situacao': 'Ativo',
        'excluido_aps': False,
        'excluido_banco': False,
        'is_active': True,
        'valor_emprestimo': 1249.11,
        'valor_parcela': 35.0,
        'quantidade_parcelas': 72,
        'parcelas_aberto': 61,
        'saldo': 1188.25,
        'taxa': 2.23
    }
]
