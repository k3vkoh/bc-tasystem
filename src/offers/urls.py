from django.urls import path, re_path
from .views import OfferCreateView, OfferListView, OfferDeleteView, OfferAcceptView, OfferDetailView, OfferRejectView

app_name = 'offers'

urlpatterns = [
    path('', OfferListView.as_view(), name='offer-list'),
    re_path(r'^create/(?P<pk>[0-9a-f-]+)/$',
            OfferCreateView.as_view(), name='offer-create'),
    re_path(r'^delete/(?P<pk>[0-9a-f-]+)/$',
            OfferDeleteView.as_view(), name='offer-delete'),
    re_path(r'^accept/(?P<pk>[0-9a-f-]+)/$',
            OfferAcceptView.as_view(), name='offer-accept'),
    re_path(r'^detail/(?P<pk>[0-9a-f-]+)/$',
            OfferDetailView.as_view(), name='offer-detail'),
    re_path(r'^reject/(?P<pk>[0-9a-f-]+)/$',
            OfferRejectView.as_view(), name='offer-reject'),
]
