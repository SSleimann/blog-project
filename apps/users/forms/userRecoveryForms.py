from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation

class RecoveryPassword(forms.Form):
    email = forms.EmailField(label=_('Email'), widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Correo"}), required=True)

class UserSetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            "autofocus": True, 
            "autocomplete": "new-password", 
            "placeholder": "Contraseña"}),
        strip=False,
    )
    
    password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autofocus": True, 
            "autocomplete": "new-password",
            "placeholder": "Confirmar contraseña"}),
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        
        try:
            password_validation.validate_password(password2, self.user)
        except forms.ValidationError as error:
            self.add_error("password2", error)
            
        return password2
    
    def save(self, commit=True):
        password = self.cleaned_data.get("password2")
        
        self.user.set_password(password)
        if commit:
            self.user.save()
            
        return self.user
    
