from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_placeholder(field,placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        add_placeholder(self.fields['username'],'Your username')
        add_placeholder(self.fields['email'],'Your e-mail')
        add_placeholder(self.fields['first_name'],'Ex.: Alex')
        add_placeholder(self.fields['last_name'],'Ex.: Winchester')
        add_placeholder(self.fields['password'],'Type your password')


    username = forms.CharField(
        label = 'Username',
        help_text = 'The length should be between 4 and 150 characters.',
        error_messages={
            'min_length': 'Username must have at least 4 characters.',
            'max_length': 'Username must have less than 150 characters.'
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required':'Write your first name'},
        label='First Name',
    )
    last_name = forms.CharField(
        error_messages={'required':'Write your last name'},
        label='Last Name',
    )
    email = forms.EmailField(
        error_messages={'required':'E-mail is required'},
        label='E-mail',
        help_text ='The e-mail must be valid'
        )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                    'placeholder':'Your password'
                                }),
                                label='Password',)
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder':'Repeat your password'
                                }),
                                label='Password2')

    class Meta:
        model= User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',]
        
        labels = {
            'username': 'Username',
            'password':'Password'
        }
        
        error_messages = {
            'username':{
                'required':'This field must not be empty',
            }
        }


    def clean_password(self):
        data = self.cleaned_data.get('password')
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

        if not regex.match(data):
            raise ValidationError(
               'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.',
                code='invalid'

            )

        return data
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email
   
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Password and Password2 must be equal',
                'password2':'Password and Password2 must be equal'
            }        
            )