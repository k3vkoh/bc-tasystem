from django.urls import path
from .views import OfferCreateView, OfferListView, OfferDeleteView, OfferDetailView

app_name = 'offers'

urlpatterns = [
    path('create/<int:pk>/', OfferCreateView.as_view(), name='offer-create'),
    path('', OfferListView.as_view(), name='offer-list'),
    path('delete/<int:pk>/', OfferDeleteView.as_view(), name='offer-delete'),
    path('detail/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
]
