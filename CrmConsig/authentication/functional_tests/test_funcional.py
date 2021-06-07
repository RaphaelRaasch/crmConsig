import time
import json
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from authentication.models import InterestedIn
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

        user_test = CreateUserForTest()  # instance of CreateUserForTest
        self.admin_user = user_test.user_admin()  # Creating an admin user
        self.normal_user = user_test.user_basic()  # creating a normal user
        self.manager_user = user_test.user_manager()  # creating a manager user

    def tearDown(self) -> None:
        self.browser.quit()

    def login_user(self):
        self.browser.find_element_by_id('id_username').send_keys('admin')
        self.browser.find_element_by_id('id_password').send_keys('password123')
        time.sleep(1)
        self.browser.find_element_by_id('id_submit_login').click()
        time.sleep(1)

    def login_default_user(self):
        self.browser.find_element_by_id('id_username').send_keys('basic')
        self.browser.find_element_by_id('id_password').send_keys('password123')
        time.sleep(1)
        self.browser.find_element_by_id('id_submit_login').click()
        time.sleep(1)

    def login_manager_user(self):
        self.browser.find_element_by_id('id_username').send_keys('manager')
        self.browser.find_element_by_id('id_password').send_keys('password123')
        time.sleep(1)
        self.browser.find_element_by_id('id_submit_login').click()
        time.sleep(1)

    # Criação de matricula por cpf
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

    # @skip('Não quero testar')
    def test_admin_access_page_and_consult_profile(self):
        self.browser.get(self.live_server_url)  # start do server
        time.sleep(1)
        self.login_user()  # Utilizando a funçao de login
        self.browser.find_element_by_id('dropdown1').click()
        # self.browser.find_element_by_id('atualizar_dados').click()
        self.browser.find_element_by_id('user_profile').click()
        time.sleep(1)
        result = self.browser.find_element_by_id('perfil_text').text

        self.assertEqual(result, 'Perfil')

    # @skip('Não quero testar')
    def test_normal_user_access_and_profile(self):
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_default_user()
        self.browser.find_element_by_id('dropdown1').click()
        self.browser.find_element_by_id('user_profile').click()
        time.sleep(1)

        self.assertEqual(
            self.browser.find_element_by_id('perfil_text').text, 'Perfil'
        )

    def test_manager_access_and_profile(self):
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.login_manager_user()
        self.browser.find_element_by_id('dropdown1').click()
        self.browser.find_element_by_id('user_profile').click()
        time.sleep(1)

        self.assertEqual(
            self.browser.find_element_by_id('perfil_text').text, 'Perfil'
        )
        self.assertEqual(
            self.browser.find_element_by_id('profile_name').text, 'manager'
        )

    # @skip('nào quero testar')
    def test_access_interest_page(self):
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.browser.find_element_by_id('id_tab_interest').click()
        self.browser.find_element_by_id('id_name').send_keys('Nome Teste')
        self.browser.find_element_by_id('id_email').send_keys('email@teste.com')
        self.browser.find_element_by_id('id_phone').send_keys('94654981579')
        self.browser.find_element_by_id('id_submit_register').click()
        time.sleep(1)

        interested = InterestedIn.objects.get(name='Nome Teste')

        self.assertEqual(interested.name, 'Nome Teste')
        self.assertEqual(interested.email, 'email@teste.com')
        self.assertEqual(interested.phone, '94654981579')

        self.assertEqual(
            self.browser.find_element_by_id('id_success_title').text, 'Registro concluído!'
        )
