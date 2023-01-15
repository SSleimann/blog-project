from django.urls import path, include

app_name = 'core'

urlpatterns = [
    path('blog/', include('apps.blog.urls')),
    path('auth/', include('apps.users.urls')),
    path('me/', include('apps.me.urls')),
]