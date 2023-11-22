from django.core.management.base import BaseCommand
from main.models import CustomUser


class Command(BaseCommand):
    help = 'Replace the real username in the email with "username@racek.com" for existing users'

    def handle(self, *args, **options):
        users = CustomUser.objects.all()

        for user in users:
            user.email = f"{user.username}@racek.com"
            user.save()

        self.stdout.write(self.style.SUCCESS('Emails updated successfully!'))
