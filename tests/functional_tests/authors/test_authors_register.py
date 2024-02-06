from .base import AuthorsBaseTest
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder ="{placeholder}"]')

    def field_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed() and not (field == form.find_element(By.NAME, 'email')):
                field.send_keys(' ' * 20)

    def test_empty_first_name_error_message(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.field_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        
        first_name_field = self.get_by_placeholder(form,'Ex.: Alex')
        first_name_field.send_keys(' ')
        first_name_field.send_keys(Keys.ENTER)
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.assertIn('Write your first name', form.text)