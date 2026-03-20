import csv
import os
import tempfile

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils import check_csv_errors


class ImportDataAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        csv_file = request.FILES.get('file')
        model_name = request.data.get('model_name')

        if not csv_file:
            return Response(
                {'detail': 'CSV file is required in "file".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not model_name:
            return Response(
                {'detail': '"model_name" is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                for chunk in csv_file.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name

            model = check_csv_errors(temp_path, str(model_name).capitalize())
            has_roll_no = any(field.name == 'roll_no' for field in model._meta.fields)

            inserted_count = 0
            skipped_count = 0

            with open(temp_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if has_roll_no and 'roll_no' in row:
                        if model.objects.filter(roll_no=row['roll_no']).exists():
                            skipped_count += 1
                            continue

                    model.objects.create(**row)
                    inserted_count += 1

            return Response(
                {
                    'detail': 'Data imported successfully.',
                    'model': model.__name__,
                    'inserted': inserted_count,
                    'skipped': skipped_count,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as error:
            return Response(
                {'detail': str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
