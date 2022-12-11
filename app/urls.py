"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, re_path, path
from login import views, forms

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    
    re_path(r'^login/$', views.CustomLogin.as_view(redirect_authenticated_user=True, template_name='users/login.html',
                                           authentication_form=forms.LoginForm), name='login'),
    re_path(r'^register/$', views.registration, name='register'),
    re_path(r'^profile/$', views.myProfile, name='profile'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'), 
    
    re_path(r'^userapi/', include('login.urls')),
    re_path(r'^posts/', include('blog.urls')),
    
    path('', views.index, name='index'),
]

