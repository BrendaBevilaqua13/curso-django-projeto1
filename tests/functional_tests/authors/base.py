from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from recipes.utils.browser import make_edge_browser
import time
from selenium.webdriver.common.by import By


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_edge_browser()
        return super().setUp()
   
   
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self,qdt=10):
        time.sleep(qdt) 

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder ="{placeholder}"]')
    
    