import subprocess
import os


class ControlFirewall:
    def __init__(self):
        self.file = 'ips-brasil-iptables.txt'

    def core(self):
        rules = self.open_file_rules()
        if rules:
            return self.allow_range_ips(rules)
            
    def open_file_rules(self):
        rules = []
        if os.path.isfile(self.file):
            file = open(self.file)
            for _ in file:
                rules.append(file.readline()[: -1])
            return rules

        else:
            return False

    def denny_all(self):
        http = subprocess.call('iptables -A INPUT -p tcp --dport 80 -j DROP', shell=True)
        https = subprocess.call('iptables -A INPUT -p tcp --dport 443 -j DROP', shell=True)
        if http == 0 and https == 0:
            subprocess.call('iptables -A INPUT -p tcp --dport 22 -j DROP', shell=True)
            subprocess.call('iptables -A INPUT -p tcp --dport 2222 -j DROP', shell=True)
            subprocess.call('iptables -A INPUT -p tcp --dport 21 -j DROP', shell=True)
            subprocess.call('iptables -A INPUT -p tcp --dport 2121 -j DROP', shell=True)
            return True
        return False

    def allow_ssh(self):
        ssh = subprocess.call('iptables -A INPUT -p tcp --dport 22 -j ACCEPT', shell=True)
        print(ssh)
        if ssh == 0:
            return True
        return False

    def allow_range_ips(self, rules: list):
        for rule in rules:
            if subprocess.call(rule, shell=True):
                return self.refresh_iptables(rule)
            print(f"Regra adicionada {rule}")
        if self.denny_all():
            return f"Foi liberado acesso {len(rules)} e bloqueado demais ips"

    def refresh_iptables(self, rule=None):
        if subprocess.call('iptables -F', shell=True) == 0:
            return f"Erro ao adicionar a regra {rule} IPTABLES foi reiniciado"
        else:
            return 'Erro ao dar refresh IPTABLES'


if __name__ == '__main__':
    resp = ControlFirewall().core()
    print(resp)
