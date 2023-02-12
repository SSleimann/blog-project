from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash

from typing import Dict, Any

from apps.users.forms import userConfigsForms

class UserUpdateBiographyView(LoginRequiredMixin, FormView):
    ''' Change the user biography '''
    
    template_name = 'change_bio.html'
    form_class = userConfigsForms.UserUpdateBiographyForm
    success_url = reverse_lazy('core:me:meProfile')
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        
        return kwargs
    
    def form_valid(self, form):
        user = form.save()
        
        if user:
            messages.success(self.request, _('You have successfully changed your biography!'))
        
        return super().form_valid(form)
    

class UserChangePasswordView(LoginRequiredMixin, FormView):
    ''' Change the user password '''
    
    template_name = 'change_password.html'
    form_class = userConfigsForms.UserChangePasswordForm
    success_url = reverse_lazy('core:users:user_login')
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        
        return kwargs
    
    def form_valid(self, form):
        user = form.save()
        
        if user:
            messages.success(self.request, _('You have successfully changed your password.'))
        
        return super().form_valid(form)