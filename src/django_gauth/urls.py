import django_gauth.views
from django.urls import path

app_name = 'django_gauth'

urlpatterns = [
    path('google/login', django_gauth.views.google_login, name='login'),
    path('google/callback',
         django_gauth.views.google_callback, name='login_callback'),
]
