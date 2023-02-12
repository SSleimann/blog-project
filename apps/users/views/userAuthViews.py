from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views.generic import FormView

from apps.users.forms import userAuthForms

#Class views
class UserRegisterView(FormView):
    ''' Register a new user using the RegisterForm and redirects him '''
    
    template_name = 'register.html'
    form_class = userAuthForms.RegisterForm
    success_url = reverse_lazy('core:users:user_login')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            messages.add_message(self.request, messages.SUCCESS, _('You have been registered!'))
        
        return super().form_valid(form)

class UserLoginView(FormView):
    ''' Login a user using the LoginForm and redirects him '''
    
    template_name = 'login.html'
    form_class = userAuthForms.LoginForm
    success_url = reverse_lazy('core:blog:index')
    
    def form_valid(self, form):
        credentials = form.cleaned_data
        next = self.request.GET.get('next', None)
            
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
            
            return super().form_valid(form) if not next else redirect(next)
            
        messages.add_message(self.request, messages.ERROR, _('Wrong credentials, please try again'))
        return HttpResponseRedirect(reverse_lazy('core:users:user_login'))

@login_required
def userLogoutView(request):
    ''' Logs out a user session if it is open and redirects him '''
    
    logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have been logged out!'))
    
    return HttpResponseRedirect(reverse_lazy('core:users:user_login'))

