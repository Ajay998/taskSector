from django.core.management.base import BaseCommand, CommandError
import csv
from dataentry.utils import check_csv_errors
from dataentry.models import Student

# Proposed command - python manage.py importdata file_path model_name

class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def handle(self, *args, **kwargs):
        # logic goes here
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        model = check_csv_errors(file_path, model_name)
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if model.objects.filter(roll_no=row['roll_no']).exists():
                    self.stdout.write(self.style.WARNING(f"Record with roll_no {row['roll_no']} already exists. Skipping."))
                    continue
                self.stdout.write(f"Inserting data: {row}")
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS('Data imported from CSV successfully!'))