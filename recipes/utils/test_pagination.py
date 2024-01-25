from unittest import TestCase
import math

def make_pagination_range(page_range,
            qty_pages,
            current_page):
    
    middle_range = math.ceil(qty_pages/2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset
    
    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_page': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }

class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range = list(range(1, 21)),
            qty_pages = 4,
            current_page = 1
        )['pagination']
        self.assertEqual([1,2,3,4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range = list(range(1, 21)),
            qty_pages = 4,
            current_page = 6
        )['pagination']
        self.assertEqual([5,6,7,8], pagination)
    
    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range = list(range(1, 21)),
            qty_pages = 4,
            current_page = 21
        )['pagination']
        self.assertEqual([17,18,19,20], pagination)
    
    

