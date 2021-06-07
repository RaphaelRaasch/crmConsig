import requests

from CrmConsig.settings import env_config


class ConsultAPI:

    def __init__(self):
        self.__querystring = {"apikey": env_config.get('API_KEY')}

        self.__headers = {
            'cache-control': "no-cache"
        }

    def try_catch_errors(self, url, querystring):
        try:
            response = requests.request("GET", url, headers=self.__headers, params=querystring)
            return response
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None

    def cpf(self, value):
        url = f"{env_config.get('MATRICULA_URL')}{value}"
        querystring = self.__querystring
        return self.try_catch_errors(url=url, querystring=querystring)

    def matricula(self, value, real_time):
        if real_time:
            api_url = env_config.get('MATRICULA_REAL_TIME')
            querystring = {"apikey": env_config.get('API_KEY_REAL_TIME')}
        else:
            api_url = env_config.get('MATRICULA_DETALHADA_URL')
            querystring = self.__querystring

        url = f"{api_url}{value}"
        return self.try_catch_errors(url=url, querystring=querystring)
