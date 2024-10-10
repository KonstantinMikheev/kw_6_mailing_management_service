from django.conf import settings
from django.core.cache import cache

from mailing.models import Client, EmailSetting


def get_clients_from_cache():
    """
    Get clients from cache. If cache is disabled, retrieve from database.
    Returns:
        QuerySet: All clients from the database or from cache.
    """

    if not settings.CACHE_ENABLED:
        clients = Client.objects.all()
    else:
        key = 'clients'
        clients = cache.get(key)
        if clients is None:
            clients = Client.objects.all()
            cache.set(key, clients)

    return clients


def get_mailings_from_cache():
    """
    Get mailings from cache. If cache is disabled, retrieve from database.
    Returns:
        QuerySet: All email settings from the database or from cache.
    """

    if not settings.CACHE_ENABLED:
        mailings = EmailSetting.objects.all()
    else:
        key = 'mailings'
        mailings = cache.get(key)
        if mailings is None:
            mailings = EmailSetting.objects.all()
            cache.set(key, mailings)

    return mailings
