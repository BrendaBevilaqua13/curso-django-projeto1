from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse
import ipdb


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
        current = form[field].field.help_text.get(field)
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
        ('username', 'Este campo é obrigatório.'),
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


    def test_username_field_min_length_sholud_be_4(self):
        self.form_data['username'] = 'bre'
        url = reverse('create')
        response = self.client.post(url,data=self.form_data, follow=True)
        msg = 'Username must have at least 4 characters.'
        self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get('username'))

    def test_username_field_max_length_sholud_be_150(self):
        self.form_data['username'] = 'bre' * 151
        url = reverse('create')
        response = self.client.post(url,data=self.form_data, follow=True)
        msg = 'Username must have less than 150 characters.'
        self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('create')
        response = self.client.post(url,data=self.form_data, follow=True)
        msg = ('Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.')
        self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get('password'))

    def test_password_and_password2_confirmation_are_equal(self):
        self.form_data['password'] = 'abc123'
        self.form_data['password2'] = '@a123ABC123'
        url = reverse('create')
        response = self.client.post(url,data=self.form_data, follow=True)

        msg = 'Password and Password2 must be equal'

        self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get('password'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('create')
        response = self.client.post(url)
        self.assertEqual(response.status_code,404)

    
    def test_email_field_must_be_unique(self):
        url = reverse('create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'
        errors = response.context['form'].errors.get('email')
        if errors is not None:
             self.assertIn(msg,errors)
             self.assertIn(msg,response.content.decode('utf-8'))

    
    def test_author_created_can_login(self):
        url = reverse('create')

        self.form_data.update({
                    'username': 'testeuser',
                    'password': '@Bc123456',
                    'password2':'@Bc123456',
            })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testeuser',
            password='@Bc123456'
        )
        
        self.assertTrue(is_authenticated)