from .test_recipe_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe


class RecipeViewsTest(RecipeTestBase):        
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
               
     # tests de category         
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)
        
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_category_template_loads_recipes(self):
        needed_title =  'This is category test'
        self.make_recipe(title=needed_title) 
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
    
    def test_recipe_category_template_dont_load_recipes_not_published(self): 
        recipe = self.make_recipe(is_published=False) 
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)
        
    def test_recipe_datail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
    
    def test_recipe_datail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_datail_template_loads_the_correct_recipe(self):  
        needed_title =  'This is datail page'
        self.make_recipe(title=needed_title) 
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1}))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
     
    def test_recipe_datail_template_dont_load_recipe_not_published(self): 
        recipe = self.make_recipe(is_published=False) 
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.id}))

        self.assertEqual(response.status_code, 404)
        
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)
        
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?search=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        
    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?search=teste')
        self.assertIn(
            'teste',
            response.content.decode('utf-8')
        )