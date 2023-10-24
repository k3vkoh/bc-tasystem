from django.urls import path, re_path
from .views import ApplicationCreateView, ApplicationListView, ApplicationDeleteView, ApplicationDetailView, ApplicationRejectView
app_name = 'applications'

urlpatterns = [
    path('', ApplicationListView.as_view(), name='application-list'),
    re_path(r'^create/(?P<pk>[0-9a-f-]+)/$',
            ApplicationCreateView.as_view(), name='application-create'),
    re_path(r'^delete/(?P<pk>[0-9a-f-]+)/$',
            ApplicationDeleteView.as_view(), name='application-delete'),
    re_path(r'^detail/(?P<pk>[0-9a-f-]+)/$',
            ApplicationDetailView.as_view(), name='application-detail'),
    re_path(r'^reject/(?P<pk>[0-9a-f-]+)/$',
            ApplicationRejectView.as_view(), name='application-reject'),
]
