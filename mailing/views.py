from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from mailing.forms import ClientForm
from mailing.models import Mailing, Client


class MailingHomeView(ListView):
    model = Mailing
    template_name = "mailing/home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["all_mailings_count"] = Mailing.objects.count()
        context["active_mailings_count"] = Mailing.objects.filter(status="running",).count()
        context["unique_recipients_count"] = Client.objects.distinct('email').count()

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


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def get_success_url(self):
        return reverse("mailin:client_detail", args=[self.kwargs.get("pk")])

class ClientDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_delete.html"
    success_url = reverse_lazy("mailing:client_list")
