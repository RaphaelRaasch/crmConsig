from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from authentication.test.create_user_for_test import CreateUserForTest

fake = Faker()


class TestUpdateUser(TestCase):
    def setUp(self) -> None:
        user_test = CreateUserForTest()
        self.user = user_test.user_admin()
        self.password = user_test.password
        self.url_login = user_test.url_login
        self.name = fake.name()
        self.username = fake.email()
        self.data = {'username': self.username, 'password1': 'Bl@122D@', 'password2': 'Bl@122D@',
                     'role': '755', 'name': self.name, 'phone': '', 'photo': ''}
        url = '/auth/administration/new_user'
        self.client.login(username=self.user, password=self.password)
        self.client.post(url, self.data)

    def test_update_other_user(self):
        """Deve retornar pagina 403 por ser querer alterar dados de outro usuário"""
        user = User.objects.get(username=self.username)
        password = fake.uuid4()
        self.data.update({'password1': password, 'password2': password})
        resp = self.client.post(reverse('auth:atualizar_senha', kwargs={'pk': user.pk}), self.data)
        self.assertEqual(resp.status_code, 302)
        login = self.client.login(username=self.username, password=password)
        self.assertEqual(login, False)

    def test_update_user(self):
        self.client.login(username=self.username, password='Bl@122D@')
        user = User.objects.get(username=self.username)
        password = fake.uuid4()
        self.data.update({'password1': password, 'password2': password})
        resp = self.client.post(reverse('auth:atualizar_senha', kwargs={'pk': user.pk}), self.data)
        login = self.client.login(username=self.username, password=password)
        self.assertEqual(login, True)
        self.assertEqual(resp.status_code, 302)
