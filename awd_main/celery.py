import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awd_main.settings')

# Setup new Celery application for awd_main project.
app = Celery('awd_main')

# Load task modules from all registered Django app configs.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover and load tasks.py in all registered Django app configs.
app.autodiscover_tasks()

# Optional: Define a sample task to test Celery setup. (Async task example)
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')