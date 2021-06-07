from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker

from authentication.models import Usuario, Empresa
from authentication.test.create_user_for_test import CreateUserForTest

fake = Faker()


class TestCreateUser(TestCase):
    def setUp(self) -> None:
        user_test = CreateUserForTest()
        self.user = user_test.user_admin()
        self.password = user_test.password
        self.url_login = user_test.url_login
        self.name = fake.name()
        self.username = fake.email()
        self.data = {'username': self.username, 'password1': 'Bl@122D@', 'password2': 'Bl@122D@',
                     'role': '755', 'name': self.name, 'phone': '', 'photo': ''}
        self.url = '/auth/administration/new_user'

    def test_response_ok(self):
        self.client.login(username=self.user, password=self.password)
        resp = self.client.post(self.url, self.data)
        self.client.login(username=self.user, password=self.password)
        self.assertEqual(resp.status_code, 302)

    def test_create_custom_user(self):
        self.client.login(username=self.user, password=self.password)
        self.client.post(self.url, self.data)
        custom = Usuario.objects.filter(name=self.name).first()
        self.assertIsNotNone(custom)

    def test_create_user(self):
        self.client.login(username=self.user, password=self.password)
        self.client.post(self.url, self.data)
        user = User.objects.filter(username=self.username).first()
        self.assertIsNotNone(user)

    def test_foreign_key(self):
        self.client.login(username=self.user, password=self.password)
        self.client.post(self.url, self.data)
        custom = Usuario.objects.filter(name=self.name).first()
        user = User.objects.filter(pk=custom.user_id).first()
        self.assertIsNotNone(user)

    def test_block_add_user(self):
        """Deve bloquear adicionar novos usuários pois não tem mais direito a adicionar novos usuários"""
        empresa = Empresa.objects.first()
        empresa.n_user_disponiveis = 0
        empresa.save()
        self.client.login(username=self.user, password=self.password)
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.context.get('msg'),
            'Limite de usuários execido. O seu plano não tem suporte para adicionar mais usuários.'
        )
