from django.urls import path, re_path
from .views import UploadView, ListView, CloseView, CourseDetailView

app_name = 'courses'

urlpatterns = [
    path('', ListView.as_view(), name='course-list'),
    path('manage/', UploadView.as_view(), name='manage-course'),
    path('manage/archive/', CloseView.as_view(), name='archive-course'),
    re_path(r'^(?P<pk>[0-9a-f-]+)/$',
            CourseDetailView.as_view(), name='course-detail'),
]
