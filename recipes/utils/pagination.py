from django.core.paginator import Paginator
from recipes.utils.test_pagination import make_pagination_range

""" Gerador de senha
python -c "import string as s;from random import SystemRandom as sr;
print(''.join(sr().choices(s.ascii_letters + s.punctuation, k=64)))" 
"""

def make_pagination(request, queryset, per_page, qty_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
        
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page
    )

    return page_obj, pagination_range