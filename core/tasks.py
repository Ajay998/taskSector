from awd_main.celery import app
import time

@app.task
def celery_task():
    # Simulate a long-running task
    time.sleep(10)
    return "Task executed successfully!"