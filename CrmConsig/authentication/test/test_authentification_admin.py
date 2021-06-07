from django.test import TestCase
from django.urls import reverse

from authentication.test.create_user_for_test import CreateUserForTest


class TestAuthenticationUserManager(TestCase):
    def setUp(self) -> None:
        user_test = CreateUserForTest()
        self.user = user_test.user_admin()
        self.password = user_test.password
        self.url_login = user_test.url_login

    # self.client.login(username='user_test', password='temporary')
    def test_not_authentication(self):
        """Must be redirect for authentication  """
        resp = self.client.get(reverse('auth:access_basic'))
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, self.url_login)

    def test_route_with_access_basic(self):
        self.client.login(username=self.user, password=self.password)
        resp = self.client.get('/auth/')
        self.assertEqual(resp.status_code, 200)

    def test_access_route_manager(self):
        self.client.login(username=self.user, password=self.password)
        resp = self.client.get(reverse('auth:manager'))
        self.assertEqual(resp.status_code, 200)

    def test_route_with_access_admin(self):
        """Must be return status code 200"""
        self.client.login(username=self.user, password=self.password)
        resp = self.client.get(reverse('auth:administration'))
        self.assertEqual(resp.status_code, 200)
