import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from testfixtures.django import compare as django_compare

from authentication.test.create_user_for_test import CreateUserForTest
from data_consig.data_flow import DataFlow
from data_consig.models import Matricula, MatriculaDetalhada, ContratoEmprestimo, ContratoCartao


class TestUrls(TestCase, DataFlow):

    def setUp(self) -> None:
        self.cpf_url = reverse('data_consig:cpf_view')
        self.matricula_detalhada_url = reverse('data_consig:matricula_detalhada_view')

        self.cpf = '231312313'
        self.matricula = '626362236'
        self.matriculas = ['25362456465', '4523452345', '5322134245', '532352345']
        self.maxDiff = None

        for matricula in self.matriculas:
            Matricula.objects.create(
                cpf=self.cpf,
                matricula=matricula,
                inserted_by_cpf_api=True
            )

        user_test = CreateUserForTest()
        self.user = user_test.user_admin()

        self.client.login(username='admin', password='password123')

    # @skip("Não quero testar.")
    def test_post_method_cpf(self):
        response = self.client.post(self.cpf_url, {'cpf': self.cpf})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [str(matricula) for matricula in response.context['matriculas']],
            self.matriculas
        )

    # @skip("Não quero testar.")
    def test_post_method_matricula_detalhada(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.create_matricula_and_contratos_table(self.cpf, self.matricula, data)

        response = self.client.post(
            self.matricula_detalhada_url, {'matricula': self.matricula}
        )

        self.assertEqual(response.status_code, 200)
        django_compare(
            response.context['matricula_detalhada'],
            MatriculaDetalhada.objects.get(matricula=self.matricula),
            ignore_eq=True
        )
        django_compare(
            response.context['contratos_emprestimo'],
            ContratoEmprestimo.objects.filter(matricula=self.matricula),
            ignore_eq=True
        )
        django_compare(
            response.context['contratos_cartao'],
            ContratoCartao.objects.filter(matricula=self.matricula),
            ignore_eq=True
        )

    # @skip("Não quero testar.")
    def test_post_method_matricula_detalhada_real_time(self):
        with open('data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.create_matricula_and_contratos_table(self.cpf, '0706240146', data)

        response = self.client.post(
            self.matricula_detalhada_url, {'matricula': '0706240146', 'real_time': True}
        )

        today = timezone.now().date()
        month = str(today.month) if len(str(today.month)) > 2 else f'0{today.month}'
        today = f'{today.day}/{month}/{today.year}'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['matricula_detalhada'].real_time, True)
        self.assertContains(response, today)
