from django.urls import path
from .views import OfferCreateView, OfferListView, OfferDeleteView, OfferAcceptView

app_name = 'offers'

urlpatterns = [
    path('create/<int:pk>/', OfferCreateView.as_view(), name='offer-create'),
    path('', OfferListView.as_view(), name='offer-list'),
    path('delete/<int:pk>/', OfferDeleteView.as_view(), name='offer-delete'),
    path('accept/<int:pk>/', OfferAcceptView.as_view(), name='offer-accept'),
]
