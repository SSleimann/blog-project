from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^detailpost/(?P<slug>[-\w]+)/$", views.PostDetail.as_view(), name='post_detail'),
    re_path(r'^createpost/$', views.CreatePost.as_view(), name='post_create'),
    re_path(r'^deletepost/(?P<slug>[-\w]+)/$', views.delete_post, name='delete_post'),
]

