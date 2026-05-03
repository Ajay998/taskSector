import tempfile
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from ..tasks import import_data_task


class ImportDataAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def post(self, request):
        csv_file   = request.FILES.get('file')
        model_name = request.data.get('model_name')

        if not csv_file:
            return Response(
                {'detail': 'CSV file is required in "file".'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not model_name:
            return Response(
                {'detail': '"model_name" is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'detail': 'Only .csv files are allowed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if csv_file.size > self.MAX_FILE_SIZE:
            return Response(
                {'detail': 'File too large. Max size is 10MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='wb') as tmp:
            for chunk in csv_file.chunks():
                tmp.write(chunk)
            temp_path = tmp.name

        task = import_data_task.delay(temp_path, model_name)

        return Response(
            {'detail': 'Import started.', 'task_id': task.id},
            status=status.HTTP_202_ACCEPTED
        )