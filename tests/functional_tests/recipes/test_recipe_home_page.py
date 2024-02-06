from selenium.webdriver.common.by import By
import pytest
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma Receita', body.text)
        