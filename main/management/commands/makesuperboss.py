from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from main.models import CustomUser


class Command(BaseCommand):
    help = 'Assign the "superuser" group to CustomUser instances'

    def handle(self, *args, **options):
        # Get the first user based on the id
        user = CustomUser.objects.first()

        # Check if a user exists
        if user:
            group = Group.objects.get(name='Superboss')
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f'Superboss group assigned to {user.username} successfully!'))
        else:
            self.stdout.write(self.style.WARNING('No users found.'))


