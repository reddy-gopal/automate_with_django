from django.core.management.base import BaseCommand, CommandError

import csv
from django.apps import apps
class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help = 'Path to CSV file')
        parser.add_argument('model_name', type=str , help= 'Model name').capitalize()

    def handle(self, *args, **options):
        file_path = options['file_path']
        model_name = options['model_name']

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label , model_name)
                break
            except LookupError:
                continue

        if not model:
            CommandError(f"There is no model with name {model_name} in any app")
         
        with open(file_path , 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        self.stdout.write("Inserted Successfullly")