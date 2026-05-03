from awd_main.celery import app
import time
from django.core.management import call_command
from django.conf import settings


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    return 'Data imported successfully.'
