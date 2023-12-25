from unittest import TestCase
import math

def make_pagination_range(page_range,
            qty_pages,
            current_page):
    
    middle_range = math.ceil(current_page/2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset


    return page_range[start_range:stop_range]

class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range = list(range(1, 21)),
            qty_pages = 4,
            current_page = 1
        )
        self.assertEqual([1,2,3,4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range = list(range(1, 21)),
            qty_pages = 4,
            current_page = 3
        )
        self.assertEqual([2,3,4,5], pagination)