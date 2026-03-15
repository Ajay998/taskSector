from django.apps import apps
from django.core.management.base import CommandError
import csv

def check_csv_errors(file_path, model_name):
    try:
        model = apps.get_model('dataentry', model_name)
    except LookupError as error:
        raise ValueError(f"Model '{model_name}' does not exist in the 'dataentry' app.") from error

    if not model:
        raise CommandError(f'Model "{model_name}" not found in app "dataentry"!')

    # Check if the CSV file can be read and has the correct headers
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        
        # Get model fields
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']        
        # Check if all headers are present in model fields
        for header in headers:
            if header not in model_fields:
                raise ValueError(f"CSV header '{header}' does not match any field in the '{model_name}' model.")
    
    return model