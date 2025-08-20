from django.core.management.base import BaseCommand
from dataentry.utils import check_csv_errors
import csv

class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help = 'Path to CSV file')
        parser.add_argument('model_name', type=str , help= 'Name of the Model')

    def handle(self, *args, **options):
        file_path = options['file_path']
        model_name = options['model_name'].capitalize()
        try:
            model =  check_csv_errors(file_path, model_name)
        except Exception as e:
            raise str(e)
        

        with open(file_path , 'r') as file:
            reader = csv.DictReader(file)
            for data in reader:
                model.objects.create(**data)
           
        self.stdout.write("Inserted Successfullly")