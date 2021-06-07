from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from authentication.models import Usuario
from authentication.test.create_user_for_test import CreateUserForTest


class TestUserProfile(TestCase):

    def setUp(self) -> None:
        user_test = CreateUserForTest()
        self.user = user_test.user_basic()
        self.username = 'basic'
        self.password = user_test.password
        self.url_profile = reverse('auth:user_profile', kwargs={'pk': User.objects.get(username=self.username).pk})

    def test_user_profile_get_not_logged(self):
        response = self.client.get(self.url_profile)

        self.assertEqual(response.status_code, 302)

    def test_user_profile_get_logged(self):
        self.client.login(username=self.username, password=self.password)

        user_id = User.objects.get(username=self.username).pk

        user = Usuario.objects.get(user_id=user_id)
        user.name = 'Nome teste'
        user.phone = '5132452345'
        user.save()

        response = self.client.get(self.url_profile)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário comum')
        self.assertContains(response, 'Empresa Teste')
        self.assertContains(response, 'Nome teste')
        self.assertContains(response, '5132452345')
