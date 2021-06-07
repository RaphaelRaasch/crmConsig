import subprocess

import requests
from sentry_sdk import capture_message
from CrmConsig.settings import env_config
from authentication.models import IpBrasil


class ControllerAccessIps:
    """Bloqueia no iptables acesso a ips fora do Brasil"""
    def __init__(self, ip: str):
        self.endpoint = env_config.get('ENDPOINT_IPAPI')
        self.token = env_config.get('TOKEN_IPAPI')
        self.ip = ip

    def get_origin_ip(self) -> dict:
        url = f"{self.endpoint}{self.ip}?access_key={self.token}"
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()

        else:
            capture_message(f'Erro n IP API {url}', '30')
            return False

    def ip_out_brasil(self):
        qs = IpBrasil.objects.filter(ip=self.get_range_ip()).count()
        if qs != 0:
            return False
        origin = self.get_origin_ip()
        if origin.get('country_code') == 'BR':
            ip = self.get_range_ip()
            IpBrasil.objects.create(ip=ip)
            return False
        return True

    def control(self):
        if self.ip_out_brasil():
            return self.block_ip()
        return False

    def block_ip(self):
        """iptables -A INPUT -s 181.41.198.0/24 -j DROP"""
        range_ips = self.get_range_ip() + '/24'
        cmd = f"iptables -A INPUT -s {range_ips} -j DROP"
        resp = subprocess.call(cmd, shell=True)
        if resp == 0:
            return True
        else:
            msg = f"Erro ao criar a regra {cmd} no Iptables"
            capture_message(msg, '30')
            return msg

    def get_range_ip(self):
        """Pega um range de ips """
        ip = self.ip.split('.')
        ip = ".".join(x for x in ip[:-1])
        return ip


def control(ip):
    resp = ControllerAccessIps(ip).control()
    # print(f"IP {ip} Foi bloqueado ? {resp}")