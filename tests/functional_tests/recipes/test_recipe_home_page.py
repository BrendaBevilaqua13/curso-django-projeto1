from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma Receita', body.text)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_bach()

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        #usuario abre a pagina
        self.browser.get(self.live_server_url)

        #vê um input de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        #clica no input e digita o termo de busca
        #"title_needed" para encontrar a receita com esse titulo
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # o usuario ver o que estava procurando na página
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME,'main-content-list').text
        )

        
        self.sleep(3)
        