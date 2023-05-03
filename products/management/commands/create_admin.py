from django.core.management.base import BaseCommand, CommandError
from users.models import User


class Command(BaseCommand):
    help = "Creates a new admin user"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Custom username for admin"
            )
        parser.add_argument(
            "--password",
            type=str,
            help="Custom password for admin"
            )
        parser.add_argument(
            "--email",
            type=str,
            help="Custom email for admin"
            )

    def handle(self, *args, **options):
        admin_username = options["username"]
        admin_password = options["password"]
        admin_email = options["email"]

        username = admin_username if admin_username else "admin"
        password = admin_password if admin_password else "admin1234"
        email = admin_email if admin_email else f"{username}@example.com"

        check_username = User.objects.filter(username=username).first()
        check_email = User.objects.filter(email=email).first()

        if check_username:
            raise CommandError(
                f"Username `{check_username.username}` already taken."
                )
        if check_email:
            raise CommandError(
                f"Email `{check_email.email}` already taken."
                )

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
            )

        self.stdout.write(
            self.style.SUCCESS(f"Admin `{username}` successfully created!")
        )
