from django.urls import path
from .views import UploadView, ListView, DetailView

urlpatterns = [
	path('', ListView.as_view(), name='course-list'),
	path('<int:pk>/', DetailView.as_view(), name='course-detail'),
    path('upload/', UploadView.as_view(), name='upload-excel'),
]
