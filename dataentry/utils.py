from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.conf import settings
import os
import datetime
from django.db import DataError

def check_csv_errors(file_path, model_name):
    try:
        model = apps.get_model('dataentry', model_name)
    except LookupError as error:
        raise ValueError(f"Model '{model_name}' does not exist in the 'dataentry' app.") from error

    if not model:
        raise CommandError(f'Model "{model_name}" not found in app "dataentry"!')

    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
    # Check if the CSV file can be read and has the correct headers
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        csv_headers = reader.fieldnames
        if csv_headers != model_fields:
                raise DataError(f"CSV file doesn't match with the {model_name} table fields.")
    return model


def generate_csv_file(model_name):
    # generate the timestamp of current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # define the csv file name/path

    export_dir = 'exported_data'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    directory_path = os.path.join(settings.MEDIA_ROOT, export_dir)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, file_name)
    return file_path


def get_all_custom_model():
    default_models = ['ContentType', 'Permission', 'Uploads', 'Group', 'LogEntry', 'Session', 'Message', 'Upload']
    custom_models = [models.__name__ for models in apps.get_models() if models.__name__ not in default_models]
    return custom_models