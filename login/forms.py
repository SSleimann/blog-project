from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    """LoginForm definition."""
    # TODO: Define form fields here
    username = forms.CharField(max_length=150, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Search'})
        )
    
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Enter description here'}),
        }
        fields = ['username', 'password']