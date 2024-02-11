from .base import AuthorsBaseTest
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def field_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed() and not (field == form.find_element(By.NAME, 'email')):
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self,callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.field_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form,'Ex.: Alex')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)
    
    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form,'Ex.: Winchester')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form,'Your username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The length should be between 4 and 150 characters.', form.text)
        self.form_field_test_with_callback(callback)
    
    def test_empty_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form,'Your e-mail')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The e-mail must be valid', form.text)
        self.form_field_test_with_callback(callback)
    
    def test_passwords_do_not_match(self):
        def callback(form):
            password1_field = self.get_by_placeholder(form,'Type your password')
            password2_field = self.get_by_placeholder(form,'Repeat your password')
            password1_field.send_keys('P@ssw0rd')
            password2_field.send_keys('P@ssw0rd_Different')
            password2_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Password and Password2 must be equal', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form,'Ex.: Alex').send_keys('First Name')
        self.get_by_placeholder(form,'Ex.: Winchester').send_keys('Last Name')
        self.get_by_placeholder(form,'Your username').send_keys('username')
        self.get_by_placeholder(form,'Your e-mail').send_keys('email@invalid.com')
        self.get_by_placeholder(form,'Type your password').send_keys('P@ssw0rd1')
        self.get_by_placeholder(form,'Repeat your password').send_keys('P@ssw0rd1')
        
        form.submit()
        
        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )