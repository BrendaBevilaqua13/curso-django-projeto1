from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
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
        categoria = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='brenda',
            last_name='carla',
            username='brendac.',
            password='12345',
            email='brenda@gmail.com',
        )
        recipe = Recipe.objects.create(
            category = categoria,
            author = author,
            title = 'Recipe title',
            description ='Recipe description',
            slug ='Recipe slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            cover = None,
            servings_unit = 'Porções',
            preparation_steps = 'Recipe preparation_steps',
            preparation_steps_is_html = False,
            is_published = True,
        )
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_recipe_context = response.context['recipes']
        self.assertIn('Recipe title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_recipe_context), 1)
        
     
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)
        
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_datail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
    
    def test_recipe_datail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)
        
 