from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http.response import Http404, HttpResponse as HttpResponse
from recipes.utils.pagination import make_pagination
from .models import Recipe
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
import os
import ipdb

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self,*args,**kwargs):
        qs = super().get_queryset(*args,**kwargs)
        qs = qs.filter(
            is_published=True
        )

        qs = qs.select_related('author','category')

        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args,**kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get('recipes'), PER_PAGE)
        
        ctx.update(
            {'recipes':page_obj, 'pagination_range':pagination_range}
            )

        return ctx

class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes_list = list(self.get_context_data()['recipes'].object_list.values())
        return JsonResponse(recipes_list,safe=False)

class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'


    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - Category |',
        })

        return ctx

    
class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self):
        txt_search = self.request.GET.get('search')

        if not txt_search:
            raise Http404()

        qs = Recipe.objects.filter(title__icontains=txt_search,
                                   is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('search')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe_view.html'

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(is_published = True)


        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args,**kwargs)
        
        ctx.update({
            'is_detail_page':True
        })
        
        return ctx

class RecipeDetailApi(RecipeDetail):

    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri()+recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''
        
        del recipe_dict['is_published']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )