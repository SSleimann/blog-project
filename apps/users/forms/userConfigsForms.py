from django import forms
from django.utils.translation import gettext_lazy as _
from .userRecoveryForms import UserSetPasswordForm

class UserUpdateBiographyForm(forms.Form):
    biography = forms.CharField(
                                required=True,
                                label=_('Biography'), 
                                max_length=250, 
                                widget=forms.Textarea(attrs={'placeholder': 'Biografia'})
                                )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        bio = self.cleaned_data.get("biography")
        
        self.user.bio = bio
        
        if commit:
            self.user.save()
        
        return self.user
        
class UserChangePasswordForm(UserSetPasswordForm):
    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(attrs={"autofocus": True, "autocomplete": "current-password"}),
        strip=False,
    )
    
    field_order = ('old_password', 'password1', 'password2')
    
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("You have entered your old password incorrectly!"))
        
        return old_password
    
            