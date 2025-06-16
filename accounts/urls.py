from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.apps import AccountsConfig
from accounts.views import RegisterView, email_verification, PasswordResetRequestView, AccountPasswordResetConfirmView

app_name = AccountsConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='mailing:main'), name='logout'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/<str:token>/", AccountPasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]
