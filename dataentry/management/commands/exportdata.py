from django.core.management.base import BaseCommand, CommandError
import csv
from django.apps import apps
from dataentry.utils import exported_file
class Command(BaseCommand):
    help = "Export data from student model to a CSV file"


    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str , help= "which model u want to export data")


    def handle(self, *args, **options):

        model_name = options['model_name']
        model = None

        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label , model_name)
                break

            except LookupError:
                continue

        if not model:
            CommandError(f"No model with name {model_name}")
            
        data = model.objects.all()

        file_path = exported_file(model_name)

        with open(file_path , 'w', newline= '') as file:
            writer = csv.writer(file)

            writer.writerow([field.name for field in model._meta.fields])

            for dt in data:
                writer.writerow([ getattr(dt , field.name)  for field in model._meta.fields])

        self.stdout.write("Exporting completed")