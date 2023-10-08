from django.urls import path
from .views import ApplicationCreateView

urlpatterns = [
    path('application/create/<int:pk>/', ApplicationCreateView.as_view(), name='application-create'),
]
