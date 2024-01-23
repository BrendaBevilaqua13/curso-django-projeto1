from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


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

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@gmail.com',
            'password': 'Strong@password11',
            'password': 'Strong@password11',
        }

        return super().setUp(*args,**kwargs)
    

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('password','Este campo é obrigatório.'),
        ('password2','Password and Password2 must be equal'),
        ('first_name','Write your first name'),
        ('last_name','Write your last name'),
        ('email','E-mail is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('create')
        response = self.client.post(url,data=self.form_data, follow=True)
        self.assertIn(msg,response.content.decode('utf-8'))

