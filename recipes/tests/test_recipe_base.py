from django.test import TestCase
from recipes.models import Category, Recipe, User

class RecipeMixin:
     
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)
    
    
    def make_author(self,first_name='brenda',
            last_name='carla',
            username='brendac.',
            password='12345',
            email='brenda@gmail.com'):
        
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email= email
        )
    
    def make_recipe(self,
            category_data = None,
            author_data = None,
            title = 'Recipe title',
            description ='Recipe description',
            slug ='Recipe slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            cover=None,
            servings_unit = 'Porções',
            preparation_steps = 'Recipe preparation_steps',
            preparation_steps_is_html = False,
            is_published = True):
        
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        
        return Recipe.objects.create(
            category = self.make_category(**category_data),
            author = self.make_author(**author_data),
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            cover = cover,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            preparation_steps_is_html = preparation_steps_is_html,
            is_published = is_published,
        )
    
    def make_recipe_in_bach(self, qdt=10):
        recipes = []
        for i in range(qdt):
            kwargs = {'title':f'Recipe title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)

        return recipes
                


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self):
        return super().setUp()
    
   
        
    