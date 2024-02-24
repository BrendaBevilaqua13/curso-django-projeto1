from django.shortcuts import render,HttpResponse, redirect
from authors.forms import RegisterForm, LoginForm, AuthorRecipeForm
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from django.template.defaultfilters import slugify

def register_view(request):
   register_form_data = request.session.get('register_form_data', None)
   form = RegisterForm(register_form_data)
   return render(request, 'authors/pages/register_view.html',
                 {'form':form,
                  'form_action': reverse('create'),})


def register_create(request):
   if not request.POST:
      raise Http404() 
   
   POST = request.POST
   request.session['register_form_data'] = POST
   form = RegisterForm(POST)

   if form.is_valid():
      user = form.save(commit=False)
      user.password = make_password(user.password)
      user.save()
      messages.success(request,'Your user is created, please log in.')

      del(request.session['register_form_data'])
      return redirect('login')

   return redirect('register')
 

def login_view(request):
   form = LoginForm()
   return render(request, 'authors/pages/login.html',{
      'form':form,
      'form_action': reverse('login_create'), 
   })


def login_create(request):
   if not request.POST:
      raise Http404() 
   
   form = LoginForm(request.POST)
   
   if form.is_valid():
      authenticated_user = authenticate(
         username=form.cleaned_data.get('username',''),
         password=form.cleaned_data.get('password',''),
      )
      if authenticated_user is not None:
         messages.success(request, 'Your are Logged in.')
         login(request, authenticated_user)
      else:     
         messages.error(request,'Invalid credentials')
   else:
      messages.error(request,'Invalid username or password')

   return redirect('dashboard')

@login_required(login_url='login', redirect_field_name='next')
def logout_view(request):
   if not request.POST:
      messages.error(request, 'Invalid logout request')
      return redirect('login')
   
   messages.error(request,'Invalid logout user')
   if request.POST.get('username') != request.user.username:
      return redirect('login')
   
   messages.success(request,'Logged out successfully')
   logout(request)
   return redirect('login')

@login_required(login_url='login', redirect_field_name='next')
def dashboard(request):
   recipes = Recipe.objects.filter(
      is_published=False,
      author=request.user
   )
   return render(request,'authors/pages/dashboard.html',
                 {
                    'recipes':recipes
                 })

@login_required(login_url='login', redirect_field_name='next')
def dashboard_recipe_edit(request,id):
   recipe = Recipe.objects.filter(
      is_published=False,
      author=request.user,
      pk=id
   ).first()

   if not recipe:
      raise Http404()
   
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

      recipe.save()
      messages.success(request,'Sua receita foi salva com sucesso!')
      return redirect(reverse('dashboard_recipe_edit',args=(id,)))
   
   return render(request,'authors/pages/dashboard_recipe.html',
                 {
                    'form':form
                 })

def dashboard_recipe_create(request):
   if request.method == 'POST':
      POST = request.POST
      FILES = request.FILES
      form = AuthorRecipeForm(POST,FILES)
      if form.is_valid():

         recipe = form.save(commit=False)
         recipe.author = request.user
         recipe.slug = slugify(request.POST.get('title'))
         recipe.preparation_steps_is_html = False
         recipe.is_published = False
         recipe.save()

         messages.success(request,'Sua receita foi criada com sucesso!')
         return redirect('dashboard')
      else:
         return render(request,'authors/pages/dashboard_recipe.html',{'form':form})
   
   form = AuthorRecipeForm()

   return render(request,'authors/pages/dashboard_recipe.html',
                {'form':form,
                  'form_action': reverse('dashboard_recipe_create')})

@login_required(login_url='login', redirect_field_name='next')
def dashboard_recipe_delete(request):
   if not request.POST:
      raise Http404() 
   
   POST = request.POST
   id = POST.get('id')

   recipe = Recipe.objects.filter(
      is_published=False,
      author=request.user,
      pk=id
   ).first()

   if not recipe:
      raise Http404()
   
   recipe.delete()
   messages.success(request, 'Receita deletada com sucesso!')
   return redirect('dashboard')
   