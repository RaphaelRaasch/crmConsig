import json
import time
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from authentication.test.create_user_for_test import CreateUserForTest
from data_consig.data_flow import DataFlow
from data_consig.models import Matricula


class TestAccess(StaticLiveServerTestCase, DataFlow):

    def setUp(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.browser.implicitly_wait(3)

        self.cpf = '52345328475'
        self.matriculas = ['4323452', '4523453245', '25367856', '45325234']
        self.matricula_especifica = '9999988885555'

        user_test = CreateUserForTest()
        self.user = user_test.user_admin()

    def tearDown(self) -> None:
        self.browser.quit()

    def login_user(self):
        self.browser.find_element_by_id('id_username').send_keys('admin')
        self.browser.find_element_by_id('id_password').send_keys('password123')
        time.sleep(1)
        self.browser.find_element_by_id('id_submit_login').click()
        time.sleep(1)

    def create_matriculas_by_cpf(self):
        for matricula in self.matriculas:
            Matricula.objects.create(
                cpf=self.cpf,
                matricula=matricula,
                inserted_by_cpf_api=True
            )

    def matricula_detalhada_custom_tests(self):
        self.assertEqual('Karin Agari Jorgensen De Camargo', self.browser.find_element_by_id('nome_cliente').text)
        self.assertEqual('13.166,49', self.browser.find_element_by_id('valor_matricula_cliente').text)
        self.assertEqual('3213', self.browser.find_element_by_id('agencia_banco').text)
        self.assertEqual(
            'PENSAO MENSAL VITALICIA - SINDROME DA TALIDOMIDA - LEI 7070/82',
            self.browser.find_element_by_id('descricao_matricula').text
        )

        contratos_emprestimo = self.browser.find_elements_by_class_name('contrato_emprestimo')
        contratos_emprestimo = [contrato.text for contrato in contratos_emprestimo]

        self.assertEqual(
            sorted([
                '608318828', '185473494', '603404309', '813243754', '58002443410-331', '601901264',
                '25-50509/19015', '5416412', '55-6469741/19'
            ]),
            sorted(contratos_emprestimo)
        )

        contratos_cartao = self.browser.find_elements_by_class_name('contrato_cartao')
        contratos_cartao = [contrato.text for contrato in contratos_cartao]

        self.assertEqual(
            ['9108028'],
            contratos_cartao
        )

    # @skip('nào quero testar')
    def test_user_access_page_and_pass_cpf(self):
        self.create_matriculas_by_cpf()
        # O usuário acessa a url e verifica as informações da página
        self.browser.get(self.live_server_url)
        self.login_user()

        cpf = self.browser.find_element_by_id('id_cpf')
        cpf.send_keys(self.cpf)
        time.sleep(1)
        self.browser.find_element_by_id('submit_cpf').click()
        matriculas = self.browser.find_elements_by_class_name('matricula_button')
        matriculas = [matricula.text for matricula in matriculas]

        self.assertEqual(sorted(self.matriculas), sorted(matriculas))

    # @skip('nào quero testar')
    def test_user_access_page_and_pass_cpf_on_search_box(self):
        self.create_matriculas_by_cpf()
        # O usuário acessa a url e pesquisa o cpf através da barra de pesquisa superior da página
        self.browser.get(self.live_server_url)
        self.login_user()

        self.browser.find_element_by_id('search_btn_1').click()
        self.browser.find_element_by_id('search_input_1').send_keys(self.cpf)
        self.browser.find_element_by_id('search_cpf_btn').click()
        time.sleep(1)
        matriculas = self.browser.find_elements_by_class_name('matricula_button')
        matriculas = [matricula.text for matricula in matriculas]

        self.assertEqual(sorted(self.matriculas), sorted(matriculas))

    # @skip('nào quero testar')
    def test_user_access_page_and_pass_matricula(self):
        self.browser.get(self.live_server_url)  # iniciano o server
        self.login_user()
        with open(
                'data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8'
        ) as file:
            data = json.load(file)
        self.create_matricula_and_contratos_table(self.cpf, self.matricula_especifica, data)  # criei info no banco

        self.browser.find_element_by_id('id_matricula').send_keys(
            self.matricula_especifica)  # usuario envia info no input
        time.sleep(1)
        self.browser.find_element_by_id('submit_matricula').click()  # usuário faz o submit do dado

        self.matricula_detalhada_custom_tests()

    # @skip('nào quero testar')
    def test_user_access_page_and_pass_matricula_real_time(self):
        self.browser.get(self.live_server_url)  # iniciano o server
        self.login_user()
        with open(
                'data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8'
        ) as file:
            data = json.load(file)
        # Criação de informações no banco
        self.create_matricula_and_contratos_table(self.cpf, '0706240146', data)

        # O usuário envia info no input
        self.browser.find_element_by_id('id_matricula').send_keys('0706240146')
        time.sleep(1)
        self.browser.find_element_by_id('submit_matricula').click()  # usuário faz o submit do dado

        self.browser.find_element_by_id('real_time_submit').click()
        
        # O usuário clica no botão para atualização por função Real Time
        real_time_date = self.browser.find_element_by_id('real_time_date').text
        today = timezone.now().date()
        month = str(today.month) if len(str(today.month)) > 2 else f'0{today.month}'
        today = f'{today.day}/{month}/{today.year}'

        self.assertEqual(real_time_date, today)

    # @skip('nào quero testar')
    def test_user_search_button_matricula_detalhada(self):
        self.browser.get(self.live_server_url)  # iniciano o server
        self.login_user()
        with open(
                'data_consig/tests/api_matricula/test_json/NB_-_706240146.json', 'r', encoding='utf-8'
        ) as file:
            data = json.load(file)
        self.create_matricula_and_contratos_table(self.cpf, self.matricula_especifica, data)  # criei info no banco

        self.browser.find_element_by_id('search_btn_1').click()
        self.browser.find_element_by_id('search_input_1').send_keys(
            self.matricula_especifica
        )  # usuario envia info no input
        time.sleep(1)
        self.browser.find_element_by_id('search_matricula_btn').click()  # usuário faz o submit do dado

        self.matricula_detalhada_custom_tests()
