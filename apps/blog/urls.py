from django.urls import re_path, include
from . import views

app_name = 'blog'

urlpatterns = [
    # re_path(r"^index/$", views.CreateAndListPosts.as_view(), name="index"),
    re_path(r"^index/$", views.index, name="index"),
    re_path(r"^deletepost/(?P<slug>[-\w]+)/$", views.PostDeleteView.as_view(), name="delete_post"),
    re_path(r"^detailpost/(?P<slug>[-\w]+)/$", views.PostDetailView.as_view(), name="detail_post"),
]