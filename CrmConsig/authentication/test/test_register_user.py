from django.test import TestCase
from django.urls import reverse

from authentication.models import InterestedIn


class TestRegisterUser(TestCase):

    def setUp(self) -> None:
        # self.login_url = 'accounts/login/'
        self.login_url = reverse('login')
        self.signup_url = reverse('auth:signup')

    def test_get_method_login(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)

    def test_post_method_signup(self):
        data = {
            'name': 'Nome Teste',
            'phone': '4323562423',
            'email': 'test@gmail.com'
        }
        response = self.client.post(self.signup_url, data)

        db_interested = InterestedIn.objects.get(name='Nome Teste')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(db_interested.name, 'Nome Teste')
        self.assertEqual(db_interested.phone, '4323562423')
        self.assertEqual(db_interested.email, 'test@gmail.com')
