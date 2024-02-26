from django.views import View
from recipes.models import Recipe
from django.http.response import Http404
from authors.forms.recipe_forms import AuthorRecipeForm
from django.contrib import messages
from django.shortcuts import redirect,render
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import ipdb


@method_decorator(
            login_required,name='dispatch'
    )
class DashboardRecipe(View):
    recipe = None

    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe
    
    def render_recipe(self,form):
        
        return render(self.request,'authors/pages/dashboard_recipe.html',
                        {
                            'form':form
                        })


    
    def get(self, request, id=None):
        recipe = self.get_recipe(id)     
        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)
    
    def post(self,request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            #form valido e posso tentar salvar

            recipe = form.save(commit=False)

            recipe.author=request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            
            if id is None:
                recipe.slug = slugify(request.POST.get('title'))

            recipe.save()
            messages.success(request,'Sua receita foi salva com sucesso!')
            return redirect(reverse('dashboard_recipe_edit',args=(recipe.id,)))
        
        return self.render_recipe(form)