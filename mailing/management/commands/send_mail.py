from django.core.management import BaseCommand

from mailing.utils import send_mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mailing()
