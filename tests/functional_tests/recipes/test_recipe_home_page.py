from selenium.webdriver.common.by import By
from base import *


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):

        self.browser.get(self.live_server_url)
        self.sleep()
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma Receita', body.text)
        