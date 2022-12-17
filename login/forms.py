from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    """LoginForm definition."""
    # TODO: Define form fields 

    username = forms.CharField(label='', max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Usuario', 
                                      'id': 'username',                       
                                      'name': 'username',
                                      'autofocus': True }))
    
    password = forms.CharField(label='', max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                                                                               'id': 'password',
                                                                                               'name': 'password'}))
    
    remember_me = forms.BooleanField(label='Recuérdame', required=False, widget=forms.CheckboxInput(attrs={
        'id': 'remember',
        'name': 'remember-me'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]
    
    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']
        icons = {'username': 'user',
                 'password': 'lock-alt'}

class SingUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]
    
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre',
                                                                              'autofocus': True})) 

    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))

    user_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))

    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Correo'}))

    password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Contraseña'}))

    password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Confirmar contraseña'}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "user_name", "email", "password1", "password2"]
        icons = {
            'first_name': 'user-detail',
            'last_name': 'user-detail',
            'user_name': 'user',
            'email': 'envelope',
            'password1': 'lock',
            'password2': 'lock'
            }

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise ValidationError("This email already used")
        return data

    def save(self, commit=True):
        user = super(SingUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
        return user
    
