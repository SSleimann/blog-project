from django.urls import re_path

from . import views

app_name = 'me'

urlpatterns = [
    re_path(r"^profile/$", views.me_profile, name="meProfile"),
    re_path(r"^userprofile/(?P<id>\d+)/$", views.user_profile, name="userProfile"),
    re_path(r"^follow/(?P<id>\d+)/$", views.follow, name="follow"),
]