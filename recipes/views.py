from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http.response import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from recipes.utils.pagination import make_pagination
from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('id')

    page_obj, pagination_range = make_pagination(request, recipes, 10)

    return render(request, 'recipes/pages/home.html',
                   context={'recipes': page_obj,
                            'pagination_range':pagination_range})


def category(request,category_id):        
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('id'))
    page_obj, pagination_range = make_pagination(request, recipes, 10)
    
    return render(request, 'recipes/pages/category.html',
                  context={'recipes': page_obj,
                           'pagination_range':pagination_range,
                           'title': f'{recipes[0].category.name} - Category| '
                           })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    
    return render(request, 'recipes/pages/recipe_view.html',
                  {'recipe': recipe, 'is_detail_page': True})

def search(request):
    search_term = request.GET.get('search', '').strip()
    
    if not search_term:
        raise Http404()  

    recipes = Recipe.objects.filter(
        Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, 10)

    return render(request, 'recipes/pages/search.html',
                   {'page':search_term,
                    'recipes':page_obj,
                    'pagination_range':pagination_range,
                    'additional_url_query':f'&search={search_term}',
                    })