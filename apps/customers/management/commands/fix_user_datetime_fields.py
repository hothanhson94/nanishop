from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Fix datetime fields stored as strings in User model'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            updated = False

            if isinstance(user.last_login, str):
                parsed_date = parse_datetime(user.last_login)
                if parsed_date:
                    user.last_login = parsed_date
                    updated = True

            if isinstance(user.date_joined, str):
                parsed_date = parse_datetime(user.date_joined)
                if parsed_date:
                    user.date_joined = parsed_date
                    updated = True

            if updated:
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Fixed datetime for user ID {user.id}'))
            else:
                self.stdout.write(f'No changes needed for user ID {user.id}')
