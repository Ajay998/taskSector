from django.urls import path
from .views import main, celery

urlpatterns = [
    path('', main, name='main'),
    path('celery/', celery, name='celery'),
]