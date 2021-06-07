from django.test import TestCase

from authentication.controller_access_ips import ControllerAccessIps


class TestControllAccessIp(TestCase):

    def test_error(self):
        """IP EUA"""
        ip = '37.218.241.6'
        resp = ControllerAccessIps(ip).control()
        self.assertIsInstance(resp, str)

    def test_ip_brasil(self):
        """IP BR deve retornar false"""
        ip = '179.127.130.254'
        resp = ControllerAccessIps(ip).control()
        self.assertEqual(resp, False)