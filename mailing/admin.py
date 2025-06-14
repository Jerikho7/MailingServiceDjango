from django.contrib import admin

from .models import Client, Message, Mailing, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name')
    search_fields = ('email', 'full_name')
    list_filter = ('email',)
    ordering = ('email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject')
    search_fields = ('subject',)
    ordering = ('subject',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_mailing', 'end_mailing', 'message_display')
    list_filter = ('status',)
    search_fields = ('message__subject',)
    filter_horizontal = ('clients',)
    date_hierarchy = 'start_mailing'

    @admin.display(description='Тема письма')
    def message_display(self, obj):
        return obj.message.subject


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'status', 'attempted_at')
    list_filter = ('status', 'attempted_at')
    search_fields = ('server_response',)
