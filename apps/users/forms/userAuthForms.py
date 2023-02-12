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

    password1 = forms.CharField(label=_('Password'), 
                                strip=False, 
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'autofocus': True})
                                        
    )
    
    password2 = forms.CharField(label=_('Password confirmation'), 
                                strip=False, 
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'autofocus': True})
    )
        
    class Meta:
        """Meta definition for Registerform."""
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        icons = {
            'first_name': 'user-detail',
            'last_name': 'user-detail',
            'username': 'user',
            'email': 'envelope',
            'password1': 'lock',
            'password2': 'lock'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Primer nombre', 'autofocus': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Primer apellido', 'autofocus': True}),
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'autofocus': True}),
            'email': forms.TextInput(attrs={'placeholder': 'Correo', 'autofocus': True}),

        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        
        password_validation.validate_password(password2)
        
        return password2
    
    def save(self, commit=True):
        password = self.cleaned_data.get("password2")
        
        user = super().save(commit=False)
        user.set_password(password)
        
        if commit:
            user.save()
            
        return user
    
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password2", error)

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
    
