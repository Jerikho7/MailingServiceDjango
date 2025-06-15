from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import MailingHomeView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, \
    MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingSendView, \
    MailingAttemptView, ActiveMailingsView

app_name = MailingConfig.name

urlpatterns = [
    path("main/", MailingHomeView.as_view(), name="main"),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/new/", ClientCreateView.as_view(), name="client_create"),
    path("client/<int:pk>/edit/", ClientUpdateView.as_view(), name="client_update"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/new/", MessageCreateView.as_view(), name="message_form"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing_list/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/new/", MailingCreateView.as_view(), name="mailing_form"),
    path("mailing/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing/<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    path("mailing/report/", MailingAttemptView.as_view(), name="report"),
    path("mailing/active/", ActiveMailingsView.as_view(), name="active_mailing"),
]
