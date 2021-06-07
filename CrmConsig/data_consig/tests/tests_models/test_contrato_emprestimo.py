import json

from django.test import TestCase

from data_consig.data_treatment.models_treatment.contrato_emprestimo_treatment import ContratoEmprestimoTreatment
from data_consig.data_treatment.models_treatment.matricula_detalhada_treatment import MatriculaDetalhadaTreatment
from data_consig.models import Matricula, MatriculaDetalhada, ContratoEmprestimo
from data_consig.tests.api_matricula.expected_dict.contrato_emprestimo import (
    EXPECTED_NB_5466201169, EXPECTED_NB_706240146
)


class TestContratoEmprestimo(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        undesirable_columns = ['created_at', 'updated_at']
        self.__model_keys = [
            field.attname for field in ContratoEmprestimo._meta.fields
            if field.attname not in undesirable_columns
        ]

    @staticmethod
    def create_matricula_detalhada(data):
        treated_data = MatriculaDetalhadaTreatment(data).treat_and_retrieve()
        db_matricula = Matricula.objects.create(
            cpf=treated_data.get('cpf'),
            matricula=treated_data.get('matricula_id')
        )
        treated_data['matricula_id'] = db_matricula
        return MatriculaDetalhada.objects.create(**treated_data)

    def manipulate_and_create_contrato(self, data):
        matricula_detalhada = self.create_matricula_detalhada(data)

        treated_data = ContratoEmprestimoTreatment(data).treat_and_retrieve()
        for contrato_treated in treated_data:
            contrato_treated['matricula_id'] = matricula_detalhada
            ContratoEmprestimo.objects.create(**contrato_treated)
        contratos = ContratoEmprestimo.objects.filter(matricula=data.get('beneficio'))
        return [
            {
                key: value for key, value in contrato.__dict__.items() if key in self.__model_keys
            } for contrato in contratos
        ]

    # @skip("Não quero testar")
    def test_create_and_get_objects_706240146(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        contratos_list = self.manipulate_and_create_contrato(data)
        expected = EXPECTED_NB_706240146.EXPECTED_DICT_706240146
        for contrato in expected:
            contrato['codigo_emprestimo'] = str(contrato['codigo_emprestimo'])
        self.assertEqual(
            sorted(contratos_list, key=lambda value: value['contrato']),
            sorted(expected, key=lambda value: value['contrato'])
        )

    # @skip("Não quero testar")
    def test_create_and_get_objects_5466201169(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_5466201169.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        contratos_list = self.manipulate_and_create_contrato(data)
        expected = EXPECTED_NB_5466201169.EXPECTED_DICT_5466201169
        for contrato in expected:
            contrato['codigo_emprestimo'] = str(contrato['codigo_emprestimo'])
        self.assertEqual(
            sorted(contratos_list, key=lambda value: value['contrato']),
            sorted(expected, key=lambda value: value['contrato'])
        )

    # @skip("Não quero testar")
    def test_create_and_get_objects_5466201169_with_error(self):
        with open('data_consig/tests/api_matricula/test_json/NB_5466201169_error.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        contratos_list = self.manipulate_and_create_contrato(data)
        expected = EXPECTED_NB_5466201169.EXPECTED_DICT_5466201169
        for contrato in expected:
            contrato['codigo_emprestimo'] = str(contrato['codigo_emprestimo'])
        self.assertEqual(
            sorted(contratos_list, key=lambda value: value['contrato']),
            sorted(expected, key=lambda value: value['contrato'])
        )

    def test_delete_matricula_drops_contrato_emprestimo(self):
        with open('data_consig/tests/api_matricula/test_json/NB_5466201169_error.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        contratos_list = self.manipulate_and_create_contrato(data)

        contratos_database = ContratoEmprestimo.objects.filter(matricula='5466201169')
        self.assertEqual(len(contratos_database), 7)

        Matricula.objects.get(matricula='5466201169').delete()
        self.assertRaises(
            Matricula.DoesNotExist,
            Matricula.objects.get,
            matricula=contratos_list[0].get('matricula_id')
        )
        contratos_database = ContratoEmprestimo.objects.filter(matricula='5466201169')
        self.assertEqual(len(contratos_database), 0)
