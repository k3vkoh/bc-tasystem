from django.urls import path, re_path
from .views import RegisterView, ProfileView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    # path('update/<int:pk>', ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^update/(?P<pk>[0-9a-f-]+)/$', ProfileView.as_view(), name='profile'),
]
