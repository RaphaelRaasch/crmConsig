from django.test import TestCase

from authentication.test.create_user_for_test import CreateUserForTest


class TestCreateNewUser(TestCase):
    def setUp(self) -> None:
        self.user_test = CreateUserForTest()

    def test_create_user(self):
        user = self.user_test.user_admin()
        self.client.login(username=user, password=self.user_test.password)
        resp = self.client.get('/auth/administration/new_user')
        self.assertEqual(resp.status_code, 200)
