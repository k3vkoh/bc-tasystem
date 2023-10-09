from django.urls import path
from .views import UploadView, ListView, CloseView

urlpatterns = [
	path('', ListView.as_view(), name='course-list'),
    path('manage/', UploadView.as_view(), name='manage-course'),
    path('manage/archive/', CloseView.as_view(), name='archive-course'),
]
