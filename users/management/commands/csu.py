from django.conf import settings
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            telegram_id=settings.TELEGRAM_USER_ID,
            is_staff=True,
            is_superuser=True
        )
        user.set_password('12345')
        user.save()