from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingListView, contacts, ClientListView, MailingDetailView, ClientDetailView, \
    LogsListView, MailingDeleteView, MailingCreateView, ClientCreateView, MailingUpdateView, off, ClientDeleteView, \
    ClientUpdateView, HomePageView

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(HomePageView.as_view()), name='home'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_create', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_confirm_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_confirm_delete'),
    path('mailing_detail/off/<int:pk>/', off, name='off'),

    path('contacts/', contacts, name='contacts'),

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_confirm_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_confirm_delete'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),

    path('logs_list/', LogsListView.as_view(), name='logs_list'),
]
