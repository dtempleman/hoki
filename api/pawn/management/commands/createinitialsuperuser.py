import os

from django.contrib.auth.management.commands import createsuperuser


class Command(createsuperuser.Command):
    help = "Create a superuser, and exit gracefully if username already exists."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        database = "default"  # os.getenv("POSTGRES_DB")
        exists = (
            self.UserModel._default_manager.db_manager(database)
            .filter(username=username)
            .exists()
        )
        if exists:
            self.stdout.write(f"User {username} already exists, exiting normally.")
            return

        super(Command, self).handle(*args, **options)
