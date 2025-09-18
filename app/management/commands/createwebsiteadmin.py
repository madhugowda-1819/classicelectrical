# myapp/management/commands/createwebsiteadmin.py

from django.core.management.base import BaseCommand
from app.models import WebsiteAdmin
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Creates a WebsiteAdmin user (for website login)'

    def handle(self, *args, **kwargs):
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = input('Enter password: ')
        confirm = input('Confirm password: ')

        if password != confirm:
            self.stdout.write(self.style.ERROR('Passwords do not match!'))
            return

        if WebsiteAdmin.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('Username already exists!'))
            return

        if WebsiteAdmin.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR('Email already registered!'))
            return

        WebsiteAdmin.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        self.stdout.write(self.style.SUCCESS(f'WebsiteAdmin user "{username}" created successfully!'))
