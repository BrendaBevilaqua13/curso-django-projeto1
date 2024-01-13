from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_placeholder(field,placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        add_placeholder(self.fields['username'],'Your username')
        add_placeholder(self.fields['email'],'Your e-mail')
        add_placeholder(self.fields['first_name'],'Ex.: Alex')
        add_placeholder(self.fields['last_name'],'Ex.: Winchester')


    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder':'Repeat your password'
                                }))

    class Meta:
        model= User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',]
        
        labels = {
            'username': 'Username',
            'first_name':'First Name',
            'last_name': 'Last Name',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'The e-mail must be valid',
        }
        error_messages = {
            'username':{
                'required':'This field must not be empty',
            }
        }

        widgets = {
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite "atenção" no campo password',
                code='invalid'

            )

        return data
    
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