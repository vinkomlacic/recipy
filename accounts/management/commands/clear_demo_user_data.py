from django.conf import settings
from django.core.management import BaseCommand

from accounts.models import RecipyUser


class Command(BaseCommand):
    help = 'Clears all data for the demo user.'

    def handle(self, *args, **options):
        username = settings.DEMO_USER['username']

        demo_user_qs = RecipyUser.objects.filter(username=username)
        if not demo_user_qs.exists():
            self.stderr.write('Demo user does not exist.')
        else:
            demo_user = demo_user_qs.first()
            demo_user.recipes.all().delete()
            self.stdout.write('Successfully deleted demo user data.')
