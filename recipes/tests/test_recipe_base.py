from django.test import TestCase
from recipes.models import Category, Recipe, User

class RecipeTestBase(TestCase):
    def setUp(self):
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
        return super().setUp()
        
    