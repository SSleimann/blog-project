from django.urls import re_path, include

from apps.users.views import userAuthViews, userRecoveryViews, userConfigsViews

app_name = 'users'

urlpatterns = [
    re_path(r"^login/$", userAuthViews.UserLoginView.as_view(), name='user_login'),
    re_path(r"^logout/$", userAuthViews.userLogoutView, name='user_logout'),
    re_path(r"^register/$", userAuthViews.UserRegisterView.as_view(), name='user_register'),
    
    re_path(r"^passrecovery/$", userRecoveryViews.UserPassRecoveryView.as_view(), name='password_recovery'),
    re_path(r"^passrecoveryready/$", userRecoveryViews.UserPassRecoveryReadyView.as_view(), name='password_recovery_ready'),
    re_path(r"^passrecoveryconf/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[^/]+)/$", userRecoveryViews.UserPassRecoveryConfirmView.as_view(), name='password_recovery_conf'),

    re_path(r"^changebio/$", userConfigsViews.UserUpdateBiographyView.as_view(), name='change_bio'),
    re_path(r"^changepassword/$", userConfigsViews.UserChangePasswordView.as_view(), name='change_password'),
]

