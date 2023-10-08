from django.urls import path
from .views import ApplicationCreateView, ApplicationListView
app_name = 'applications'

urlpatterns = [
    path('create/<int:pk>/', ApplicationCreateView.as_view(), name='application-create'),
    path('', ApplicationListView.as_view(), name='application-list'),
]
