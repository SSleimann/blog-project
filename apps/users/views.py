from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views.generic import FormView

from . import forms

# Create your views here.
class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('core:blog:index')
    
    def form_valid(self, form):
        credentials = form.cleaned_data
            
        user = authenticate(self.request, 
                            username=credentials.get('email'),
                            password=credentials.get('password')) 
        
        remember_me = credentials.get('remember_me')
        
        if user is not None:
            if not remember_me:
                self.request.session.set_expiry(10 * 60)
                self.request.session.modified = True
            
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, _('You have been logged in!'))
            return HttpResponseRedirect(self.success_url)
            
        else:
            messages.add_message(self.request, messages.ERROR, _('Wrong credentials\
                please try again'))
            return HttpResponseRedirect(reverse_lazy('core:users:user_login'))
        

class UserRegisterView(FormView):
    template_name = 'register.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('core:users:user_login')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            messages.add_message(self.request, messages.SUCCESS, _('You have been registered!'))
            return HttpResponseRedirect(self.success_url)
        
        return super().form_valid(form)


@login_required
def userLogoutView(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have been logged out!'))
    return HttpResponseRedirect(reverse_lazy('core:users:user_login'))
