from django.core.management import BaseCommand
from accounts.models import RecipyUser
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates demo user if one does not exist.'

    def handle(self, *args, **options):
        username = settings.DEMO_USER['username']
        password = settings.DEMO_USER['password']

        if RecipyUser.objects.filter(username=username).exists():
            self.stdout.write('Demo user already exists.')
        else:
            RecipyUser.objects.create_user(username, password=password)
            msg = f'Successfully created demo user. Login using the following '
            msg += f'credentials: username - "{username}", '
            msg += f'password - "{password}". '
            self.stdout.write(msg)
