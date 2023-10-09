from django.urls import path
from .views import OfferCreateView

app_name = 'offers'

urlpatterns = [
    path('create/<int:pk>/', OfferCreateView.as_view(), name='offer-create'),
]
