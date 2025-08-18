from django.core.management.base import BaseCommand, CommandError

import csv
from django.apps import apps
from django.db import DataError
class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help = 'Path to CSV file')
        parser.add_argument('model_name', type=str , help= 'Name of the Model')

    def handle(self, *args, **options):
        file_path = options['file_path']
        model_name = options['model_name'].capitalize()

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label , model_name)
                break
            except LookupError:
                continue

        if not model:
            CommandError(f"There is no model with name {model_name} in any app")

        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        print(model_fields)
        with open(file_path , 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            if csv_header !=  model_fields:
                raise DataError(f"CSV file does not match with {model_name} fields..")
            for row in reader:
                model.objects.create(**row)
        self.stdout.write("Inserted Successfullly")