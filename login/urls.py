from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^followuser/(?P<usrname>\D+)/$', views.followuser, name='followuser'),
]


