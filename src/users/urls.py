from django.urls import path, re_path, include
from .views import ProfileView
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    re_path(r'^update/(?P<pk>[0-9a-f-]+)/$',
            ProfileView.as_view(), name='profile'),
]
