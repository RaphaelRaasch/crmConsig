import csv
import requests
from requests.api import request

url = 'https://kolmeya.com.br/api/v1/sms/store'

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer y5g8sN3XPkxQ82pNU67x54VC7axKoTeBjU6YzwLd"
}

with open('modelo.csv', 'r') as arquivo:
    dados = [x for x in csv.DictReader(arquivo)]
    index = 0
    for dado in dados:
        msg = dado['Nome']
        messages = {
            "messages": [
                {
                    "phone": 31991595159,
                    "message": f"teste de envio {msg}",
                }
        ]
        }
        response = requests.post(url=url, headers=headers, json=messages)

        if response.status_code > 200:
            print("Request Failed")
        else:
            print(response.status_code)

