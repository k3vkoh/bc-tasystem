from django.urls import path
from .views import ApplicationCreateView

app_name = 'applications'

urlpatterns = [
    path('create/<int:pk>/', ApplicationCreateView.as_view(), name='application-create'),
]
