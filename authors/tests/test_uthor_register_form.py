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

    @parameterized.expand([
       ('first_name','First Name'),
       ('last_name','Last Name'), 
       ('username','Username'),
       ('email','E-mail'),
       ('password','Password'),
       ('password2','Password2'),
    ])
    def test_labels_is_correct(self, field, label):
        form = RegisterForm()
        current_label= form[field].field.label
        self.assertEqual(label, current_label)