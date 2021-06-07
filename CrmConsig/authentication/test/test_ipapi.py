import requests
from django.test import TestCase
from CrmConsig.settings import env_config


class TestIPAPI(TestCase):
    def setUp(self) -> None:
        self.endpoint = env_config.get('ENDPOINT_IPAPI')
        self.token = env_config.get('TOKEN_IPAPI')

    def test_response_api(self):
        """BR Brazil Brasil Rio Grande do Sul RS Gravataí 94000 -29.9091 -50.953"""
        ip = '179.127.130.254'
        url = f"{self.endpoint}{ip}?access_key={self.token}"
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_ip_out_brasil(self):
        """US United States Estados Unidos Florida FL Miami 33132 25.7806 -80.1826"""
        ip = '37.218.241.6'
        url = f"{self.endpoint}{ip}?access_key={self.token}"
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)
        resp = resp.json()
        self.assertEqual(resp.get('country_code'), 'US')

    def test_get_ip_in_brasil(self):
        """BR Brazil Brasil Rio Grande do Sul RS Gravataí 94000 -29.9091 -50.953
        181.41.203.0/24
        """
        ip = '179.127.130.254'
        url = f"{self.endpoint}{ip}?access_key={self.token}"
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)
        resp = resp.json()
        self.assertEqual(resp.get('country_code'), 'BR')

    def test_ip6(self):
        ip6 = '2001:0DB8:AD1F:25E2:CADE:CAFE:F0CA:84C1'
        url = f"{self.endpoint}{ip6}?access_key={self.token}"
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)

