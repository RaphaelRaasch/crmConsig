import json

from django.test import TestCase

from data_consig.data_treatment.models_treatment.contrato_emprestimo_treatment import ContratoEmprestimoTreatment
from data_consig.tests.api_matricula.expected_dict.contrato_emprestimo import (
    EXPECTED_NB_1040179875, EXPECTED_NB_5466201169, EXPECTED_NB_706240146
)


class TestContratoEmprestimoTreatment(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_treated_output_706240146(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8') as file:
            data_706240146 = json.load(file)
        treated_dicts = ContratoEmprestimoTreatment(data_706240146).treat_and_retrieve()
        for treated_dict in treated_dicts:
            treated_dict['is_active'] = True
        self.assertEqual(treated_dicts, EXPECTED_NB_706240146.EXPECTED_DICT_706240146)

    def test_treated_output__5466201169_with_error(self):
        with open('data_consig/tests/api_matricula/test_json/NB_5466201169_error.json', 'r', encoding='utf-8') as file:
            data_5466201169_error = json.load(file)
        treated_dicts = ContratoEmprestimoTreatment(data_5466201169_error).treat_and_retrieve()
        for treated_dict in treated_dicts:
            treated_dict['is_active'] = True
        expected = EXPECTED_NB_5466201169.EXPECTED_DICT_5466201169
        self.assertEqual(treated_dicts, expected)

    def test_treated_output_5466201169(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_5466201169.json', 'r', encoding='utf-8') as file:
            data_5466201169 = json.load(file)
        treated_dicts = ContratoEmprestimoTreatment(data_5466201169).treat_and_retrieve()
        for treated_dict in treated_dicts:
            treated_dict['is_active'] = True
        self.assertEqual(treated_dicts, EXPECTED_NB_5466201169.EXPECTED_DICT_5466201169)

    def test_treated_output_1040179875(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_1040179875.json', 'r', encoding='utf-8') as file:
            data_1040179875 = json.load(file)
        treated_dicts = ContratoEmprestimoTreatment(data_1040179875).treat_and_retrieve()
        for treated_dict in treated_dicts:
            treated_dict['is_active'] = True
        self.assertEqual(treated_dicts, EXPECTED_NB_1040179875.EXPECTED_DICT_1040179875)
