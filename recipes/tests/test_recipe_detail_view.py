from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe


class RecipeDetailViewTest(RecipeTestBase):        
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.RecipeDetail)
    
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_detail_template_loads_the_correct_recipe(self):  
        needed_title =  'This is datail page'
        self.make_recipe(title=needed_title) 
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk':1}))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
     
    def test_recipe_detail_template_dont_load_recipe_not_published(self): 
        recipe = self.make_recipe(is_published=False) 
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': recipe.id}))

        self.assertEqual(response.status_code, 404)
        