from django.urls import path
from .views import ApplicationCreateView, ApplicationListView, ApplicationDeleteView, ApplicationDetailView, ApplicationRejectView
app_name = 'applications'

urlpatterns = [
    path('create/<int:pk>/', ApplicationCreateView.as_view(), name='application-create'),
    path('', ApplicationListView.as_view(), name='application-list'),
    path('delete/<int:pk>/', ApplicationDeleteView.as_view(), name='application-delete'),
    path('detail/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('reject/<int:pk>/', ApplicationRejectView.as_view(), name='application-reject'),
]
