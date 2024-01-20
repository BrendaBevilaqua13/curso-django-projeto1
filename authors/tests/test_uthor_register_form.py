from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUniTest(TestCase):
    @parameterized.expand([
       ('first_name','Ex.: Alex'),
       ('last_name','Ex.: Winchester'), 
       ('username','Your username'),
       ('email','Your e-mail'),
       ('password','Type your password'),
       ('password2','Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
       ('email','The e-mail must be valid'),
    ])
    def test_fields_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)