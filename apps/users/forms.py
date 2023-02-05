from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation

class RegisterForm(forms.ModelForm):
    """Form definition for Register."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())
            
        for field_name, field in self.fields.items():
                if field_name in icons:
                    field.icon = icons[field_name]

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre',
                                                                              'autofocus': True})) 

    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))

    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))

    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Correo'}))

    password1 = forms.CharField(label=_('Password'), 
                                strip=False, 
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
                                        
    )
    
    password2 = forms.CharField(label=_('Password confirmation'), 
                                strip=False, 
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'})
    )
        
    class Meta:
        """Meta definition for Registerform."""
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'bio')
        icons = {
            'first_name': 'user-detail',
            'last_name': 'user-detail',
            'username': 'user',
            'email': 'envelope',
            'password1': 'lock',
            'password2': 'lock'
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        
        return password1
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Correo"}), required=True)
    
    password = forms.CharField(
        label="",
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Contraseña"}),
    )
    
    remember_me = forms.BooleanField(label=_('Recordarme'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icons = getattr(self.Meta, 'icons', dict())

        for field_name, field in self.fields.items():
            if field_name in icons:
                field.icon = icons[field_name]
    
    class Meta:
        icons = {'email': 'envelope',
                 'password': 'lock-alt'}
    
class RecoveryPassword(forms.Form):
    email = forms.EmailField(label=_('Email'), widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Correo"}), required=True)

class UserSetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    
    password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        
        password_validation.validate_password(password2, self.user)
        
        return password2
    
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["password2"])
        if commit:
            self.user.save()
            
        return self.user
    
