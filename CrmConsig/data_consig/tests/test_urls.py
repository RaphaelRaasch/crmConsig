from unittest import skip

from django.test import TestCase
from django.urls import reverse

from authentication.test.create_user_for_test import CreateUserForTest


class TestUrls(TestCase):

    def setUp(self) -> None:
        self.cpf_url = reverse('data_consig:cpf_view')
        self.matricula_detalhada_url = reverse('data_consig:matricula_detalhada_view')

        self.cpf = '231312313'
        self.matricula = '626362236'

        user_test = CreateUserForTest()
        self.user = user_test.user_admin()

    # @skip('Não quero testar!')
    def test_get_method_cpf(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get(self.cpf_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cpf.html')

    # @skip('Não quero testar!')
    def test_get_method_cpf_403(self):
        response = self.client.get(self.cpf_url)

        self.assertEqual(response.status_code, 302)

    # @skip('Não quero testar!')
    def test_get_method_matricula_detalhada_403(self):
        response = self.client.get(self.matricula_detalhada_url)

        self.assertEqual(response.status_code, 302)

    # @skip('Não quero testar!')
    def test_post_method_cpf(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(self.cpf_url, {'cpf': self.cpf})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cpf.html')

    # @skip('Não quero testar!')
    def test_get_method_matricula_detalhada(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get(self.matricula_detalhada_url)

        self.assertEqual(response.status_code, 302)

    @skip('Não quero testar!')
    def test_post_method_matricula_detalhada(self):
        self.client.login(username='admin', password='password123')
        response = self.client.post(
            self.matricula_detalhada_url, {'matricula': self.matricula}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matricula_detalhada.html')
