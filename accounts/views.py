import secrets
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, ListView, DetailView, UpdateView
from django.views import View

from accounts.forms import UserRegisterForm, PasswordResetRequestForm, CustomSetPasswordForm
from accounts.models import User
from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False

        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/accounts/email-confirm/{token}"

        send_mail(
            subject="Подтверждение регистрации",
            message=f"Перейдите по ссылке для активации аккаунта: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("accounts:login"))


class PasswordResetRequestView(FormView):
    template_name = "accounts/password_reset_request.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            token = secrets.token_hex(16)
            user.token = token
            user.save()
            host = self.request.get_host()
            url = f"http://{host}/accounts/password-reset-confirm/{token}/"
            send_mail(
                subject="Сброс пароля",
                message=f"Перейдите по ссылке для сброса пароля: {url}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            messages.success(self.request, "Инструкции по сбросу пароля отправлены на ваш email.")
        else:
            messages.warning(self.request, "Пользователь с таким email не найден.")
        return super().form_valid(form)


class AccountPasswordResetConfirmView(FormView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("accounts:login")

    def get_user(self, token):
        return get_object_or_404(User, token=token)

    def get(self, request, token):
        user = self.get_user(token)
        form = self.form_class(user=user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, token):
        user = self.get_user(token)
        form = self.form_class(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            user.token = None
            user.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    permission_required = "accounts.can_view_all_users"


class UserBlockView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "accounts.can_block_users"

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.error(request, "Нельзя заблокировать самого себя.")
            return redirect("accounts:user_list")
        user.is_active = False
        user.save()
        messages.success(request, f"Пользователь {user.email} заблокирован.")
        return redirect("accounts:user_list")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/user_detail.html"
    context_object_name = "viewed_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_own_profile"] = self.object == self.request.user
        return context


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserRegisterForm
    template_name = "accounts/user_edit.html"

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse("accounts:user_detail", kwargs={"pk": self.object.pk})
