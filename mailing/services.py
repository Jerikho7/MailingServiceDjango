from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Client, Message


def get_clients_from_cache():
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = 'client_list'
    clients = cache.get(key)
    if clients:
        return clients
    clients = Client.objects.all()
    cache.set(key, clients)
    return clients


def get_messages_from_cache():
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = 'message_list'
    messages = cache.get(key)
    if messages:
        return messages
    messages = Message.objects.all()
    cache.set(key, messages)
    return messages


def get_mailings_from_cache():
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = 'mailing_list'
    mailings = cache.get(key)
    if mailings:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings