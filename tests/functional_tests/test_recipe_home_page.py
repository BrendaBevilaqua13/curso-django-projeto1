import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from recipes.utils.browser import make_edge_browser
from selenium.webdriver.common.by import By

class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_edge_browser()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, seconds=3):
        time.sleep(seconds)

class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):

        self.browser.get(self.live_server_url)
        self.sleep()
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma Receita', body.text)
        