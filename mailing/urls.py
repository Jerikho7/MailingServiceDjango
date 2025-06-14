from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingHomeView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path("main/", MailingHomeView.as_view(), name="main"),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path("client/new/", ClientCreateView.as_view(), name="client_create"),
    path("client/<int:pk>/edit/", ClientUpdateView.as_view(), name="client_update"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
]
