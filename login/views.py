from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
# Create your views here.

class UserLogin(LoginView):
    template_name = 'users/login.html'
    
@login_required
def index(request):
    return render(request, 'index.html')