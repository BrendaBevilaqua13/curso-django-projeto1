from django import forms
from recipes.models import Recipe
from recipes.utils.django_forms import add_attr
from collections import defaultdict
from django.core.exceptions import ValidationError
from recipes.utils.strings import is_positive_number

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'),'class', 'span-2')
        add_attr(self.fields.get('cover'),'class', 'span-2')


    class Meta:
        model = Recipe
        fields=['title','description','preparation_time',\
        'preparation_time_unit','servings','servings_unit',\
        'preparation_steps','cover','category']
        widgets={
            'cover':forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit':forms.Select(
                choices=(
                    ('Porções','Porções'),
                    ('Pedaços','Pedaços'),
                    ('Fatias','Fatias'),
                    ('Pessoas','Pessoas'),
                ),
            ),
            'preparation_time_unit':forms.Select(
                choices=(
                    ('Minutos','Minutos'),
                    ('Horas','Horas'),
                ),
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 chars.')

        return title

    def clean(self):
        super_clean = super().clean()
        title = super_clean.get('title')
        description = super_clean.get('description')
        if title == description:
            self._my_errors['title'].append('Cannot be equal to description'),
            self._my_errors['description'].append('Cannot be equal to title')
        
        if self._my_errors:
            raise ValidationError(self._my_errors)
    
    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append('Must be a positive number')

        return preparation_time
    
    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if not is_positive_number(servings):
            self._my_errors['servings'].append('Must be a positive number')

        return servings
    
    
