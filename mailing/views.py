from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from mailing.forms import ClientForm, MessageForm
from mailing.models import Mailing, Client, Message


class MailingHomeView(ListView):
    model = Mailing
    template_name = "mailing/home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["all_mailings_count"] = Mailing.objects.count()
        context["active_mailings_count"] = Mailing.objects.filter(
            status="running",
        ).count()
        context["unique_recipients_count"] = Client.objects.distinct("email").count()

        return context


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def get_success_url(self):
        return reverse("mailing:client_detail", args=[self.kwargs.get("pk")])


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_delete.html"
    success_url = reverse_lazy("mailing:client_list")


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_success_url(self):
        return reverse("mailing:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing/message_delete.html"
    success_url = reverse_lazy("mailing:message_list")
