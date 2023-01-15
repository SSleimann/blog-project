from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class RegisterForm(forms.ModelForm):
    """Form definition for Register."""
    password1 = forms.CharField(label=_('Password'), 
                                strip=False, 
                                required=True,
                                widget=forms.PasswordInput
    )
    
    password2 = forms.CharField(label=_('Password confirmation'), 
                                strip=False, 
                                required=True,
                                widget=forms.PasswordInput
    )
    
    class Meta:
        """Meta definition for Registerform."""
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'bio', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}), required=True)
    
    password = forms.CharField(
        label=_("Password"),
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    
    remember_me = forms.BooleanField(label=_('Remember me'), required=False)
    
