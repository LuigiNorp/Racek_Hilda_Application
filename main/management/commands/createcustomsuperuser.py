from django.contrib.auth.management.commands.createsuperuser import Command as CreatesuperuserCommand
from django.core.management.base import CommandError


class Command(CreatesuperuserCommand):
    help = 'Create a superuser with automatically generated email'

    def handle(self, *args, **options):
        email = f'temporal@racek.com'
        options['email'] = email
        super().handle(*args, **options)
        self.stdout.write(self.style.SUCCESS(f'Superuser created successfully! Email: {email}'))
