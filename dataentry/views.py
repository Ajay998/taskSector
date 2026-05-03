from django.shortcuts import render, redirect
from .utils import get_all_custom_model
from .models import Upload
from django.conf import settings
from .tasks import import_data_task
from django.contrib import messages
from .utils import check_csv_errors
import logging

logger = logging.getLogger(__name__)

def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        logger.info("Received file upload: %s", file_path.name)
        model_name = request.POST.get('model_name')
        logger.info("Selected model for import: %s", model_name)
        upload = Upload.objects.create(file=file_path, model_name=model_name)
        relative_path = upload.file.url
        logger.info("File saved to: %s", relative_path)
        base_url = settings.BASE_DIR
        logger.info("Base URL: %s", base_url)
        file_path = str(base_url) + str(relative_path)
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')

        # Trigger the Celery task to import data asynchronously
        import_data_task.delay(file_path, model_name)
        messages.success(request, 'Data import has been initiated. You will be notified once it is completed.')

        return redirect('import_data')
    else:
        custom_models = get_all_custom_model()
        context = {
            'custom_models': custom_models
        }
    return render(request, 'dataentry/importData.html', context=context)