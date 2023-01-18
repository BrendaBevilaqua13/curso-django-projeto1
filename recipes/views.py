from django.shortcuts import render


def home(request):
    return render(request, 'recipes/pages/home.html', {'nome': 'Brenda'})


def recipe(request, id):
    return render(request, 'recipes/pages/recipe_view.html', {'nome': 'Brenda'})
