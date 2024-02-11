from .base import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        str_password = 'pass'
        user = User.objects.create_user(username='my_user',password=str_password)

        # usuario abre a pagina de login
        self.browser.get(self.live_server_url + '/authors/login/')

        #usuario ver o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        #usuario digita seu usuario e senha

        username_field.send_keys(user.username)
        password_field.send_keys(str_password)

        #usuario envia o formulario
        form.submit()

        #usuario ver a mensagem de sucesso e seu nome
        self.assertIn(f'Your are logged in with {user.username}.',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
    
    def test_login_create_raises_404_if_not_post_method(self):
        self.browser.get(self.live_server_url + '/authors/login/create/')

        self.assertIn('Not Found',
                      self.browser.find_element(By.TAG_NAME,'body').text)


    def test_login_data_invalid_view_message_error(self):
        str_password = '  '
        user = User.objects.create_user(username='    ',password=str_password)
        self.browser.get(self.live_server_url + '/authors/login/')

        #usuario ver o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(str_password)

        form.submit()

        self.assertIn('Invalid username or password',
                      self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_login_user_authenticated_view_message_error(self):
        # usuario abre a pagina de login
        self.browser.get(self.live_server_url + '/authors/login/')

        #usuario ver o formulario de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys('brenda')
        password_field.send_keys('bre@1d')

        form.submit()

        self.assertIn('Invalid credentials',
                      self.browser.find_element(By.TAG_NAME, 'body').text)
