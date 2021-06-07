import json
from unittest import skip

from django.test import TestCase

from data_consig.consult_apis import ConsultAPI


class TestConsultApi(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    @skip('Não quer testar')
    def test_request_cpf(self):
        resultado_json = ConsultAPI().cpf('02149518805')
        status_code = resultado_json.status_code
        resultado_json = json.loads(resultado_json.text)
        with open(
                'data_consig/tests/api_cpf/test_json/CPF_-_021.495.188-05.json',
                'r', encoding='utf-8'
        ) as file:
            expected_json = json.load(file)

        self.assertEqual(status_code, 200)
        self.assertEqual(resultado_json['beneficios'][0]['beneficio'], expected_json['beneficios'][0]['beneficio'])
        self.assertEqual(resultado_json['cpf'], expected_json['cpf'])
        self.assertEqual(resultado_json['beneficios'][0]['nome'], expected_json['beneficios'][0]['nome'])

    @skip('Não quer testar')
    def test_request_matricula(self):
        resultado_json = ConsultAPI().matricula('1040179875')
        status_code = resultado_json.status_code
        resultado_json = json.loads(resultado_json.text)
        with open(
                'data_consig/tests/api_matricula/test_json/NB_-_1040179875.json',
                'r', encoding='utf-8'
        ) as file:
            expected_json = json.load(file)

        self.assertEqual(status_code, 200)
        self.assertEqual(resultado_json['beneficio'], expected_json['beneficio'])
        self.assertEqual(resultado_json['cpf'], expected_json['cpf'])
        self.assertEqual(resultado_json['nome'], expected_json['nome'])

    @skip('Não quer testar')
    def test_request_matricula_real_time(self):
        resultado_json = ConsultAPI().matricula('1040179875', True)  # pesquisando uma matrícula com True para real time
        status_code = resultado_json.status_code  # verifico o status code da consulta a API
        resultado_json = json.loads(resultado_json.text)  # carrego o arquivo JSON recebido
        with open(
                'data_consig/tests/api_matricula/test_json/NB_-_1040179875.json',
                'r', encoding='utf-8'
        ) as file:
            expected_json = json.load(file)

        self.assertEqual(status_code, 200)
        self.assertEqual(resultado_json['beneficio'], expected_json['beneficio'])
        self.assertEqual(resultado_json['cpf'], expected_json['cpf'])
        self.assertEqual(resultado_json['nome'], expected_json['nome'])
