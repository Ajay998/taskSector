from django.shortcuts import render
from django.http import HttpResponse
from .tasks import celery_task

def main(request):
    return render(request, 'main.html')

def celery(request):
    celery_task.delay()
    return HttpResponse("<h3>Celery is set up and running!</h3>")