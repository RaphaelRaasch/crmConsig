from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from authentication.models import Usuario
from authentication.test.create_user_for_test import CreateUserForTest

fake = Faker()


class TestManagerUser(TestCase):
    def setUp(self) -> None:
        user_test = CreateUserForTest()
        self.user = user_test.user_admin()
        self.password = user_test.password
        self.url_login = user_test.url_login
        self.name = fake.name()
        self.username = fake.email()
        self.data = {'username': self.username, 'password1': 'Bl@122D@', 'password2': 'Bl@122D@',
                     'role': '755', 'name': self.name, 'phone': '', 'photo': ''}
        url = reverse('auth:new_user')
        self.client.login(username=self.user, password=self.password)
        self.client.post(url, self.data)

    def test_list_user(self):
        resp = self.client.get(reverse('auth:list_user'))
        self.assertTemplateUsed(resp, 'listar_usuarios.html')

    def test_update_user(self):
        user = Usuario.objects.get(name=self.name)
        self.data.update({'role': '444'})
        resp = self.client.post(f"/auth/administration/update_user/{user.user_id}", self.data)
        self.assertEqual(resp.status_code, 302)
        user = Usuario.objects.get(name=self.name)
        self.assertEqual(user.role, 444)

    def test_delete_user(self):
        user = Usuario.objects.get(name=self.name)
        resp = self.client.get(f"/auth/administration/delete_user/{user.user_id}")
        self.assertEqual(resp.status_code, 302)
        usuario = Usuario.objects.filter(name=self.name).count()
        user = User.objects.filter(username=self.name).count()
        self.assertEqual(usuario, 0)
        self.assertEqual(user, 0)

    def test_block_autoremove(self):
        user = Usuario.objects.get(name=self.user)
        resp = self.client.get(f"/auth/administration/delete_user/{user.user_id}")
        self.assertEqual(resp.status_code, 302)
        usuario = Usuario.objects.get(name=self.user)
        user = User.objects.get(username=self.user)
        self.assertIsNotNone(user)
        self.assertIsNotNone(usuario)
