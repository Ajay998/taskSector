from django.urls import include, path

from .views import import_data


urlpatterns = [
	path('import/', import_data, name='import_data'),
    ]