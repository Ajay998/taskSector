from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from dataentry.utils import generate_csv_file

class Command(BaseCommand):
    help = 'Exports data from the database to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='The name of the model to export')

    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        try:
            model = apps.get_model('dataentry', model_name)
        except LookupError as error:
            raise CommandError(f'Model "{model_name}" not found in app "dataentry"!') from error
        
        data = model.objects.all()
        if not data:
            self.stdout.write(self.style.WARNING(f'No data found for model "{model_name}". Exporting an empty CSV file.'))

        file_path = generate_csv_file(model_name)

        # Write data to CSV
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([field.name for field in model._meta.fields]) # Write headers
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])
        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))