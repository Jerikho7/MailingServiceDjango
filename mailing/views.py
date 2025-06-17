from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView, TemplateView,
)

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.mixins import UserOrManagerViewAccessMixin, UserOnlyEditMixin
from mailing.models import Mailing, Client, Message, MailingAttempt


class MailingHomeView(ListView):
    model = Mailing
    template_name = "mailing/home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["all_mailings_count"] = Mailing.objects.count()
        context["active_mailings_count"] = Mailing.objects.filter(status="running",).count()
        context["unique_recipients_count"] = Client.objects.distinct("email").count()
        return context


class ClientListView(UserOrManagerViewAccessMixin, ListView):
    model = Client
    template_name = "mailing/client_list.html"

    def get_queryset(self):
        if self.request.user.has_perm('mailing.view_client'):
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)


class ClientDetailView(DetailView):
    model = Client
    template_name = "mailing/client_detail.html"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserOnlyEditMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:client_list")

    def get_success_url(self):
        return reverse("mailing:client_detail", args=[self.kwargs.get("pk")])


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = "mailing/client_delete.html"
    success_url = reverse_lazy("mailing:client_list")

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return client.user == user

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав на удаление этого клиента.")


class MessageListView(UserOrManagerViewAccessMixin, ListView):
    model = Message
    template_name = "mailing/message_list.html"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(user=self.request.user)


class MessageDetailView(DetailView):
    model = Message
    template_name = "mailing/message_detail.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserOnlyEditMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_success_url(self):
        return reverse("mailing:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def test_func(self):
        message = self.get_object()
        user = self.request.user
        return message.user == user

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав на удаление этого сообщения.")


class MailingListView(UserOrManagerViewAccessMixin, ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"

    def get_queryset(self):
        if self.request.user.has_perm('mailing.can_view_all_mailings'):
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)

class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing/mailing_detail.html"



class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UserOnlyEditMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        status = form.cleaned_data.get('status')
        if status:
            self.object.status = status
            self.object.save(update_fields=['status'])
        return response

    def get_success_url(self):
        return reverse("mailing:mailing_detail", args=[self.kwargs.get("pk")])


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        return mailing.user == user or user.has_perm('mailing.mailing_delete')

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав на удаление этой рассылки.")


class MailingAttemptView(ListView):
    model = MailingAttempt
    template_name = "mailing/report.html"
    context_object_name = "attempts"

    def get_queryset(self):
        return MailingAttempt.objects.filter(mailing__user=self.request.user)

    def get_context_data(self, **kwargs):
        """Добавление переменных в шаблон страницы статистики"""
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["total_attempts_count"] = queryset.count()
        context["success_attempts_count"] = queryset.filter(status="success").count()
        context["failed_attempts_count"] = queryset.filter(
            status="fail"
        ).count()
        return context


class MailingSendView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, user=self.request.user)
        process_mailing(mailing)
        messages.success(request, "Рассылка отправлена.")
        return redirect('mailing:mailing_detail', pk=pk)



class ActiveMailingsView(UserOrManagerViewAccessMixin, ListView):
    model = Mailing
    template_name = "mailing/active_mailing.html"
    context_object_name = "active_mailings"

    def get_queryset(self):
        queryset = Mailing.objects.filter(status="running", user=self.request.user).prefetch_related("clients", "message")
        for mailing in queryset:
            total = mailing.clients.count()
            sent = MailingAttempt.objects.filter(mailing=mailing, status="success").count()
            mailing.progress = round((sent / total) * 100) if total > 0 else 0
        return queryset

    def get_queryset(self):
        if self.request.user.has_perm('mailing.can_view_all_active_mailings'):
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)

class MailingDisableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'mailing.can_disable_mailings'

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.status = 'completed'
        mailing.save()
        messages.success(request, "Рассылка остановлена.")
        return redirect('mailing:mailing_list')
