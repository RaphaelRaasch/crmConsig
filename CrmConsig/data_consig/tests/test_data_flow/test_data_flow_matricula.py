import json
from datetime import timedelta
from unittest import skip

from django.test import TestCase
from django.utils import timezone
from testfixtures.django import compare as django_compare

from data_consig.data_flow import DataFlow
from data_consig.data_treatment.models_treatment.contrato_cartao_treatment import ContratoCartaoTreatment
from data_consig.data_treatment.models_treatment.contrato_emprestimo_treatment import ContratoEmprestimoTreatment
from data_consig.data_treatment.models_treatment.matricula_detalhada_treatment import MatriculaDetalhadaTreatment
from data_consig.models import Matricula, MatriculaDetalhada, ContratoEmprestimo, ContratoCartao
from data_consig.tests.api_matricula.expected_dict.contrato_cartao.EXPECTED_DF_706240146 import (
    EXPECTED_DICT_706240146 as expected_contrato_cartao
)
from data_consig.tests.api_matricula.expected_dict.contrato_emprestimo.EXPECTED_DF_706240146 import (
    EXPECTED_DICT_706240146 as expected_contrato_emprestimo
)
from data_consig.tests.api_matricula.expected_dict.matricula_detalhada.EXPECTED_DF_706240146 import (
    EXPECTED_DICT_706240146 as expected_matricula_detalhada
)


# noinspection PyTypeChecker,PyTypeChecker
class TestMatriculaDetalhadaDataFlow(TestCase):
    def setUp(self) -> None:
        self.matricula_pesquisada = '0706240146'
        self.data = DataFlow(matricula=self.matricula_pesquisada)
        self.maxDiff = None

    def create_matricula_detalhada(self):
        Matricula.objects.create(
            cpf='02149518805',
            matricula=self.matricula_pesquisada
        )

        with open('data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        treated_data = MatriculaDetalhadaTreatment(data).treat_and_retrieve()

        treated_data['matricula_id'] = Matricula.objects.get(matricula=self.matricula_pesquisada)

        MatriculaDetalhada.objects.create(**treated_data)

        return data

    def create_contrato(self, data, matricula_detalhada, treatment_function, model):
        treated_data = treatment_function(data).treat_and_retrieve()
        for contrato_treated in treated_data:
            contrato_treated['matricula_id'] = matricula_detalhada
            model.objects.create(**contrato_treated)

    def create_matricula_and_contratos_table(self):
        data = self.create_matricula_detalhada()

        matricula_detalhada = MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada)

        self.create_contrato(data, matricula_detalhada, ContratoEmprestimoTreatment, ContratoEmprestimo)
        self.create_contrato(data, matricula_detalhada, ContratoCartaoTreatment, ContratoCartao)

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_valid_time_stamp(self):
        self.create_matricula_and_contratos_table()
        with open(
                'data_consig/tests/api_matricula/test_json/fake_result_matricula_detalhada_1.json',
                'r', encoding='utf-8'
        ) as file:
            data = json.load(file)

        self.assertEqual(
            str(MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada).matricula),
            self.matricula_pesquisada
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(information['matricula_detalhada'],
                         MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada))
        self.assertEqual(
            information['contratos_emprestimo'].__dict__,
            ContratoEmprestimo.objects.filter(matricula=self.matricula_pesquisada).__dict__
        )
        self.assertEqual(
            information['contratos_cartao'].__dict__,
            ContratoCartao.objects.filter(matricula=self.matricula_pesquisada).__dict__
        )

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_valid_time_stamp_real_time(self):
        self.create_matricula_and_contratos_table()
        with open(
                'data_consig/tests/api_matricula/test_json/fake_result_matricula_detalhada_1.json',
                'r', encoding='utf-8'
        ) as file:
            data = json.load(file)

        self.assertEqual(
            str(MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada).matricula),
            self.matricula_pesquisada
        )

        MatriculaDetalhada.objects.filter(matricula=self.matricula_pesquisada).update(
            updated_at=timezone.now() - timedelta(31)
        )

        information = DataFlow(matricula=self.matricula_pesquisada, real_time=True).get_information(resultado=data)

        matricula_detalhada = information['matricula_detalhada'].__dict__
        contratos_emprestimos = [i.__dict__ for i in information['contratos_emprestimo']]
        contratos_cartoes = [i.__dict__ for i in information['contratos_cartao']]

        self.assertEqual(matricula_detalhada['updated_at'].date(), timezone.now().date())

        fields_to_ignore = ['_state', 'updated_at', 'created_at']
        for key in fields_to_ignore:
            del matricula_detalhada[key]
            for value in contratos_emprestimos:
                del value[key]
            for value in contratos_cartoes:
                del value[key]

        expected_matricula_detalhada['real_time'] = True
        self.assertEqual(
            matricula_detalhada,
            expected_matricula_detalhada
        )
        self.assertEqual(
            sorted(contratos_emprestimos, key=lambda k: k['contrato']),
            sorted(expected_contrato_emprestimo, key=lambda k: k['contrato'])
        )
        self.assertEqual(
            sorted(contratos_cartoes, key=lambda k: k['contrato']),
            sorted(expected_contrato_cartao, key=lambda k: k['contrato'])
        )

    def get_information_with_objects_and_invalid_time_stamp(self, file_name):
        self.create_matricula_and_contratos_table()
        MatriculaDetalhada.objects.filter(matricula=self.matricula_pesquisada).update(
            updated_at=timezone.now() - timedelta(31)
        )
        with open(
                f'data_consig/tests/api_matricula/test_json/{file_name}.json',
                'r', encoding='utf-8'
        ) as file:
            data = json.load(file)

        matricula_detalhada_antiga = MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada)
        contratos_cartoes_antigos = ContratoCartao.objects.filter(matricula=self.matricula_pesquisada)
        contratos_cartoes_antigos = [i.__dict__ for i in contratos_cartoes_antigos]
        contratos_emprestimos_antigos = ContratoEmprestimo.objects.filter(matricula=self.matricula_pesquisada)
        contratos_emprestimos_antigos = [i.__dict__ for i in contratos_emprestimos_antigos]

        self.assertEqual(
            str(matricula_detalhada_antiga),
            self.matricula_pesquisada
        )

        information = self.data.get_information(resultado=data)

        self.assertNotEqual(information['matricula_detalhada'].genero, matricula_detalhada_antiga.genero)
        contratos_emprestimos = [i.__dict__ for i in information['contratos_emprestimo']]
        self.assertNotEqual(
            contratos_emprestimos,
            contratos_emprestimos_antigos
        )
        contratos_cartoes = [i.__dict__ for i in information['contratos_cartao']]
        self.assertNotEqual(
            contratos_cartoes,
            contratos_cartoes_antigos
        )

        django_compare(
            information['matricula_detalhada'],
            MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada),
            ignore_eq=True
        )

        # Verificação de igualdade entre ContratoEmprestimo
        django_compare(
            information['contratos_emprestimo'],
            ContratoEmprestimo.objects.filter(matricula=self.matricula_pesquisada, is_active=True),
            ignore_eq=True
        )

        # Verificação de igualdade entre ContratoCartao
        django_compare(
            information['contratos_cartao'],
            ContratoCartao.objects.filter(matricula=self.matricula_pesquisada, is_active=True),
            ignore_eq=True
        )

        return information

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_invalid_time_stamp_1(self):
        information = self.get_information_with_objects_and_invalid_time_stamp('fake_result_matricula_detalhada_1')

        self.assertEqual(
            ['55-6469741/19'],
            [
                contrato.contrato for contrato in
                ContratoEmprestimo.objects.filter(matricula=self.matricula_pesquisada, is_active=False)
            ]
        )

        matricula_detalhada = information['matricula_detalhada'].__dict__
        contratos_emprestimos = [i.__dict__ for i in information['contratos_emprestimo']]
        contratos_cartoes = [i.__dict__ for i in information['contratos_cartao']]
        fields_to_ignore = ['_state', 'updated_at', 'created_at']
        for key in fields_to_ignore:
            del matricula_detalhada[key]
            for value in contratos_emprestimos:
                del value[key]
            for value in contratos_cartoes:
                del value[key]
        self.assertEqual(
            matricula_detalhada,
            expected_matricula_detalhada
        )
        self.assertEqual(
            sorted(contratos_emprestimos, key=lambda k: k['contrato']),
            sorted(expected_contrato_emprestimo, key=lambda k: k['contrato'])
        )
        self.assertEqual(
            sorted(contratos_cartoes, key=lambda k: k['contrato']),
            sorted(expected_contrato_cartao, key=lambda k: k['contrato'])
        )

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_invalid_time_stamp_2(self):
        self.get_information_with_objects_and_invalid_time_stamp('fake_result_matricula_detalhada_2')

        self.assertEqual(
            ['55-6469741/19'],
            [
                contrato.contrato for contrato in
                ContratoEmprestimo.objects.filter(matricula=self.matricula_pesquisada, is_active=False)
            ]
        )
        self.assertEqual(
            ['9108028'],
            [
                contrato.contrato for contrato in
                ContratoCartao.objects.filter(matricula=self.matricula_pesquisada, is_active=False)
            ]
        )

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_invalid_time_stamp_3(self):
        self.get_information_with_objects_and_invalid_time_stamp('fake_result_matricula_detalhada_3')

        self.assertEqual(
            [
                '0005416412', '185473494', '25-50509/19015', '55-6469741/19',
                '58002443410-331', '601901264', '603404309', '608318828', '813243754'
            ],
            [
                contrato.contrato for contrato in
                ContratoEmprestimo.objects.filter(matricula=self.matricula_pesquisada, is_active=False)
            ]
        )
        self.assertEqual(
            [],
            [
                contrato.contrato for contrato in
                ContratoCartao.objects.filter(matricula=self.matricula_pesquisada, is_active=False)
            ]
        )

    # @skip("Não quero testar")
    def test_get_information_with_objects_and_invalid_time_stamp_404(self):
        self.create_matricula_and_contratos_table()
        MatriculaDetalhada.objects.filter(matricula=self.matricula_pesquisada).update(
            updated_at=timezone.now() - timedelta(31)
        )
        with open(
                f'data_consig/tests/api_matricula/test_json/fake_result_matricula_detalhada_404.json',
                'r', encoding='utf-8'
        ) as file:
            data = json.load(file)

        matricula_detalhada_antiga = MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada)

        self.assertEqual(
            str(matricula_detalhada_antiga),
            self.matricula_pesquisada
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(information, {'error_msg': 'Matrícula não encontrada'})

    # @skip("Não quero testar")
    def test_get_information_without_objects_and_invalid_time_stamp_404(self):
        with open(
                f'data_consig/tests/api_matricula/test_json/fake_result_matricula_detalhada_404.json',
                'r', encoding='utf-8'
        ) as file:
            data = json.load(file)

        self.assertRaises(
            MatriculaDetalhada.DoesNotExist,
            MatriculaDetalhada.objects.get,
            matricula=self.matricula_pesquisada
        )

        information = self.data.get_information(resultado=data)

        self.assertEqual(information, {'error_msg': 'Matrícula não encontrada'})

    # @skip("Não quero testar")
    def test_get_information_without_objects_1(self):
        with open(
                f'data_consig/tests/api_matricula/test_json/fake_result_matricula_detalhada_1.json',
                'r', encoding='utf-8'
        ) as file:
            data = json.load(file)

        self.assertRaises(
            MatriculaDetalhada.DoesNotExist,
            MatriculaDetalhada.objects.get,
            matricula=self.matricula_pesquisada
        )

        information = self.data.get_information(resultado=data)

        django_compare(
            information['matricula_detalhada'],
            MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada),
            ignore_eq=True
        )

        # Verificação de igualdade entre ContratoEmprestimo
        django_compare(
            information['contratos_emprestimo'],
            ContratoEmprestimo.objects.filter(matricula=self.matricula_pesquisada),
            ignore_eq=True
        )

        # Verificação de igualdade entre ContratoCartao
        django_compare(
            information['contratos_cartao'],
            ContratoCartao.objects.filter(matricula=self.matricula_pesquisada),
            ignore_eq=True
        )

    @skip("Não quero testar")
    def test_get_information_without_objects_1_API_response(self):
        self.assertRaises(
            MatriculaDetalhada.DoesNotExist,
            MatriculaDetalhada.objects.get,
            matricula=self.matricula_pesquisada
        )

        information = self.data.get_information()

        django_compare(
            information['matricula_detalhada'],
            MatriculaDetalhada.objects.get(matricula=self.matricula_pesquisada),
            ignore_eq=True
        )

        # Verificação de igualdade entre ContratoEmprestimo
        django_compare(
            information['contratos_emprestimo'],
            ContratoEmprestimo.objects.filter(matricula=self.matricula_pesquisada),
            ignore_eq=True
        )

        # Verificação de igualdade entre ContratoCartao
        django_compare(
            information['contratos_cartao'],
            ContratoCartao.objects.filter(matricula=self.matricula_pesquisada),
            ignore_eq=True
        )
