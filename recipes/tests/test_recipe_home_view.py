from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe
from unittest.mock import patch


class RecipeHomeViewTest(RecipeTestBase):        
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
        
    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
        
    def test_recipe_home_template_shows_not_recipes_found_if_no_recipes(self):
         response = self.client.get(reverse('recipes:home'))
         self.assertIn('Nenhuma Receita', response.content.decode('utf-8')) 
         
     
    def test_recipe_home_template_loads_recipes(self): 
        self.make_recipe() 
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_recipe_context = response.context['recipes']
        
        self.assertIn('Recipe title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_recipe_context), 1)
    
    def test_recipe_home_template_dont_load_recipes_not_published(self): 
        self.make_recipe(is_published=False) 
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('Nenhuma Receita', response.content.decode('utf-8')) 
    
        for i in range(10):
            kwargs = {'slug':f'r{i}', 'author_data': {'username':f'u{i}'}}
            self.make_recipe(**kwargs) 
        
        with patch('recipes.views.PER_PAGE', new=4):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 4)
            self.assertEqual(len(paginator.get_page(2)), 4)
            self.assertEqual(len(paginator.get_page(3)), 2)
               
    