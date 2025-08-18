from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Greets Hey ???"

    def add_arguments(self, parser):
        parser.add_argument('name', type= str, help= 'Specifies User name')


    def handle(self, *args, **options):
        name = options['name']
        self.stdout.write(self.style.SUCCESS(f"Heyyy ?? {name}"))