import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from recipes.utils.browser import make_edge_browser
from recipes.tests.test_recipe_base import RecipeMixin

class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_edge_browser()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, seconds=3):
        time.sleep(seconds)