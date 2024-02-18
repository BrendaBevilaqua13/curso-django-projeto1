from django import forms
from recipes.models import Recipe
from recipes.utils.django_forms import add_attr

class AuthorRecipeCreateForm(forms.ModelForm):
    def __init__(self,*argas,**kwargs):
        super().__init__(*argas,**kwargs)

        add_attr(self.fields.get('preparation_steps'),'class', 'span-2')
        add_attr(self.fields.get('cover'),'class', 'span-2')

    class Meta:
        model= Recipe
        fields='title','description','preparation_time',\
        'preparation_time_unit','servings','servings_unit',\
        'preparation_steps','cover','category'

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