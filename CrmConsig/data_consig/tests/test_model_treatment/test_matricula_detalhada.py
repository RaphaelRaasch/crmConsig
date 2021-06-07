import json

from django.test import TestCase

from data_consig.data_treatment.models_treatment.matricula_detalhada_treatment import MatriculaDetalhadaTreatment
from data_consig.tests.api_matricula.expected_dict.matricula_detalhada import (
    EXPECTED_NB_1040179875, EXPECTED_NB_5149392886, EXPECTED_NB_5466201169, EXPECTED_NB_706240146
)


class TestMatriculaEspecificaTreatment(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

    def test_treated_output_706240146(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8') as file:
            data_706240146 = json.load(file)
        treated_dict = MatriculaDetalhadaTreatment(data_706240146).treat_and_retrieve()
        treated_dict['is_active'] = True
        self.assertEqual(treated_dict, EXPECTED_NB_706240146.EXPECTED_DICT_706240146)

    def test_treated_output__5466201169_with_error(self):
        with open('data_consig/tests/api_matricula/test_json/NB_5466201169_error.json', 'r', encoding='utf-8') as file:
            data_3 = json.load(file)
        treated_dict = MatriculaDetalhadaTreatment(data_3).treat_and_retrieve()
        treated_dict['is_active'] = True
        self.assertEqual(treated_dict, EXPECTED_NB_5466201169.EXPECTED_DICT_5466201169)

    def test_treated_output_5466201169(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_5466201169.json', 'r', encoding='utf-8') as file:
            data_5466201169 = json.load(file)
        treated_dict = MatriculaDetalhadaTreatment(data_5466201169).treat_and_retrieve()
        treated_dict['is_active'] = True
        self.assertEqual(treated_dict, EXPECTED_NB_5466201169.EXPECTED_DICT_5466201169)

    def test_treated_output_1040179875(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_1040179875.json', 'r', encoding='utf-8') as file:
            data_1040179875 = json.load(file)
        treated_dict = MatriculaDetalhadaTreatment(data_1040179875).treat_and_retrieve()
        self.assertEqual(treated_dict, EXPECTED_NB_1040179875.EXPECTED_DICT_1040179875)

    def test_treated_output_5149392886(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_5149392886.json', 'r', encoding='utf-8') as file:
            data_5149392886 = json.load(file)
        treated_dict = MatriculaDetalhadaTreatment(data_5149392886).treat_and_retrieve()
        self.assertEqual(treated_dict, EXPECTED_NB_5149392886.EXPECTED_DICT_5149392886)
