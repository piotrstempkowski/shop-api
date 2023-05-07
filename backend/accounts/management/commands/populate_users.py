from django.core.management import BaseCommand
from accounts.factories import BaseUserFactory

class Command(BaseCommand):
    help = "Populate database with users"

    def add_arguments(self, parser):
        parser.add_argument("num_of_users", type=int, nargs='?', default=None)

    def handle(self, *args, **options):
        num_of_users = options["num_of_users"]

        if num_of_users is None:
            num_of_users = int(input("How many users do you want to populate? "))

        BaseUserFactory.create_batch(num_of_users)

        self.stdout.write(self.style.SUCCESS(f"Successfully populated database with {num_of_users} users."))