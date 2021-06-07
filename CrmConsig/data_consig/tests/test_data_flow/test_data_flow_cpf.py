import json
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from data_consig.data_flow import DataFlow
from data_consig.models import Matricula


class TestCpfDataFlow(TestCase):
    def setUp(self) -> None:
        self.cpf_pesquisado = '02149518805'
        self.matriculas = ['0706240146', '356324534', '5466201169']
        self.data = DataFlow(cpf=self.cpf_pesquisado)

    def create_matriculas(self, inserted_by_cpf_api=False):
        for matricula in self.matriculas:
            Matricula.objects.create(
                cpf=self.cpf_pesquisado,
                matricula=matricula,
                inserted_by_cpf_api=inserted_by_cpf_api
            )

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_valid_timestamp(self):
        self.create_matriculas(inserted_by_cpf_api=True)
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado)],
            self.matriculas
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(
            sorted(self.matriculas),
            sorted([x.matricula for x in information['matriculas']])
        )

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_valid_timestamp_inserted_by_cpf_api_false(self):
        self.create_matriculas()
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado)],
            self.matriculas
        )

        self.data.get_information(resultado=data)

        self.assertEqual(
            sorted(self.matriculas),
            ['0706240146', '356324534', '5466201169']
        )

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_invalid_timestamp(self):
        self.create_matriculas()
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        Matricula.objects.filter(cpf=self.cpf_pesquisado).update(
            updated_at=timezone.now() - timedelta(days=31)
        )

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado)],
            self.matriculas
        )

        self.data.get_information(resultado=data)

        self.assertEqual(
            ['0706240146', '5466201169', '65436549768596'],
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado, is_active=True)]
        )
        self.assertEqual(
            ['356324534'],
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado, is_active=False)]
        )

        data['beneficios'].append({'beneficio': '356324534'})
        Matricula.objects.filter(cpf=self.cpf_pesquisado).update(
            updated_at=timezone.now() - timedelta(days=31)
        )

        self.data.get_information(resultado=data)

        self.assertEqual(
            ['0706240146', '356324534', '5466201169', '65436549768596'],
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado, is_active=True)]
        )
        self.assertEqual(
            [],
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado, is_active=False)]
        )

    # @skip("Não quero testar")
    def test_get_information_without_db_objects_and_in_API(self):
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado)],
            []
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(
            sorted([i['beneficio'] for i in data['beneficios']]),
            sorted([x.matricula for x in information['matriculas']])
        )

    # @skip("Não quero testar")
    def test_get_information_without_db_objects_and_not_in_API(self):
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_404.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf='54263134356')],
            []
        )

        information = DataFlow(cpf='54263134356').get_information(resultado=data)

        self.assertEqual(information, {'error_msg': 'CPF não encontrado'})

    # @skip("Não quero testar")
    def test_get_information_db_objects_and_not_in_API(self):
        self.create_matriculas()
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_404.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        Matricula.objects.filter(cpf=self.cpf_pesquisado).update(
            updated_at=timezone.now() - timedelta(days=31)
        )

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado)],
            self.matriculas
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(information, {'error_msg': 'CPF não encontrado'})

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado, is_active=True)],
            []
        )

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado, is_active=False)],
            ['0706240146', '356324534', '5466201169']
        )

    # @skip("Não quero testar")
    def test_get_information_without_beneficio_on_API(self):
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_2.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        information = self.data.get_information(resultado=data)

        self.assertEqual(information, {'error_msg': 'CPF não encontrado'})

    # @skip("Não quero testar")
    def test_get_information_db_and_without_beneficio_on_API(self):
        self.create_matriculas()
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_2.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        Matricula.objects.filter(cpf=self.cpf_pesquisado).update(
            updated_at=timezone.now() - timedelta(days=31)
        )

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado)],
            self.matriculas
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(list(information['matriculas']), [])

    # @skip("Não quero testar")
    def test_get_information_db_and_beneficios_on_API(self):
        self.create_matriculas()
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_3.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        Matricula.objects.filter(cpf=self.cpf_pesquisado).update(
            updated_at=timezone.now() - timedelta(days=31)
        )

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf=self.cpf_pesquisado)],
            self.matriculas
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(list(information['matriculas']), [])

    # @skip("Não quero testar")
    def test_get_information_without_db_and_beneficios_on_API(self):
        with open('data_consig/tests/api_cpf/test_json/fake_result_cpf_api_3.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.assertEqual(
            [i.matricula for i in Matricula.objects.filter(cpf='54263134356')],
            []
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(information, {'error_msg': 'CPF não encontrado'})
