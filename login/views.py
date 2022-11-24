from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import LoginForm, SingUpForm
from django.contrib.auth import login
from django.contrib import messages
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
def index(request):
    return render(request, 'index.html')