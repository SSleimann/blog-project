from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

from .forms import LoginForm, SingUpForm
from .models import Usuario, Follow
# Create your views here.

class CustomLogin(LoginView):
    form_class = LoginForm
    
    def form_valid(self, form) -> HTTPResponse:
        remember_me = form.cleaned_data.get('remember_me')
        
        if not remember_me:
            self.request.session.set_expiry(5*60)
            
            self.request.session.modified = True
            
        return super(CustomLogin, self).form_valid(form)

def registration(request):
    if request.method == "POST":
        form = SingUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Te has registrado correctamente." )
            return redirect('index')
        
        else:
            messages.error(request, 'Ocurrio un error.')
            return render (request=request, template_name="users/register.html", context={"form": form})
        
    form = SingUpForm()
    
    return render (request=request, template_name="users/register.html", context={"form": form})

@login_required
def myProfile(request):
    user = get_object_or_404(Usuario, user=request.user)
    return render(request=request, template_name='users/profile.html', context={'user': user})

@login_required
def followuser(request, usrname):
    user = get_object_or_404(User, username=usrname)
    
    user_to_follow = get_object_or_404(Usuario, user=user)
    my_user = get_object_or_404(Usuario, user=request.user)
    
    if user_to_follow != my_user:
        try:
            Follow.objects.get(user_id=my_user, following_user_id=user_to_follow).delete()
        except Follow.DoesNotExist:
            Follow.objects.create(user_id=my_user, following_user_id=user_to_follow)
    
    return redirect('profile')

@login_required
def index(request):
    return render(request, 'index.html')

