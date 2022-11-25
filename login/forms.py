from typing import Dict, Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    """LoginForm definition."""
    # TODO: Define form fields here
    username = forms.CharField(max_length=150, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Username', 
                                      'id': 'username',                       
                                      'name': 'username',
                                      'autofocus': True}))
    
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                                               'id': 'password',
                                                                                               'name': 'password'}))
    
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'remember',
        'name': 'remember-me'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class SingUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(SingUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
        return user
    
    User._meta.get_field('email')._unique = True