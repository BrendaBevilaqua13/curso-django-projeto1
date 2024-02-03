import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from recipes.utils.browser import make_edge_browser
from selenium.webdriver.common.by import By

class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):

    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_the_test(self):
        browser = make_edge_browser()

        browser.get(self.live_server_url)
        self.sleep()
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma Receita', body.text)
        browser.quit()