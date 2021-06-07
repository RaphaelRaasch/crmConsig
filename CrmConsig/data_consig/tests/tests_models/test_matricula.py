import json

from django.test import TestCase

from data_consig.models import Matricula


class TestMatricula(TestCase):

    def setUp(self) -> None:
        with open('data_consig/tests/api_cpf/test_json/CPF_-_021.495.188-05.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.cpf = data.get('cpf')
        self.matriculas = data.get('beneficios')
        self.maxDiff = None

    # @skip("Não quero testar")
    def test_create_and_get_objects(self):
        for matricula in self.matriculas:
            Matricula.objects.create(
                cpf=self.cpf,
                matricula=matricula.get('beneficio')
            )

        matriculas = Matricula.objects.filter(cpf=self.cpf)
        self.assertEqual(len(matriculas), 3)
        self.assertEqual(
            [matricula.matricula for matricula in matriculas],
            ['0706240146', '1264302786', '5466201169']
        )
