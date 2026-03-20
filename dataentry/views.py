from django.shortcuts import render, redirect
from .utils import get_all_custom_model
from .models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages

def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
        upload = Upload.objects.create(file=file_path, model_name=model_name)
        relative_path = upload.file.url
        base_url = settings.BASE_DIR
        file_path = str(base_url) + str(relative_path)
        # Call the management command to import data from the CSV file
        try:
            call_command('importdata', file_path, model_name)
            messages.success(request, "Data imported successfully.")
        except Exception as e:
            messages.error(request, f"Error importing data: {str(e)}")

        return redirect('import_data')
    else:
        custom_models = get_all_custom_model()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/importData.html', context=context)