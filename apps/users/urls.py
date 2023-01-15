from django.urls import re_path, include

from . import views

app_name = 'users'

urlpatterns = [
    re_path(r"^login/$", views.UserLoginView.as_view(), name='user_login'),
    re_path(r"^logout/$", views.userLogoutView, name='user_logout'),
    re_path(r"^register/$", views.UserRegisterView.as_view(), name='user_register')
]
