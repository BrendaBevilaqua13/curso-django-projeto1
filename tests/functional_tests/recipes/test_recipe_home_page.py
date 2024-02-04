from selenium.webdriver.common.by import By
import pytest
from .base import RecipeBaseFunctionalTest

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):

        self.browser.get(self.live_server_url)
        self.sleep()
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma Receita', body.text)
        