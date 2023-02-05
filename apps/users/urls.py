from django.urls import re_path, include

from . import views

app_name = 'users'

urlpatterns = [
    re_path(r"^login/$", views.UserLoginView.as_view(), name='user_login'),
    re_path(r"^logout/$", views.userLogoutView, name='user_logout'),
    re_path(r"^register/$", views.UserRegisterView.as_view(), name='user_register'),
    
    re_path(r"^passrecovery/$", views.UserPassRecoveryView.as_view(), name='password_recovery'),
    re_path(r"^passrecoverydone/$", views.UserPassRecoveryDoneView.as_view(), name='password_recovery_done'),
    re_path(r"^passrecoveryconf/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[\w\.-]+)/$", views.UserPassRecoveryConfirmView.as_view(), name='password_recovery_conf'),
]

