from django.core.management.base import BaseCommand
from dataentry.models import Student

# Add data to database using this command

class Command(BaseCommand):
    help = 'Inserts data into the database'

    def handle(self, *args, **kwargs):
        # Import your models here
        dataset = [
            {'roll_no': 1002, 'name': 'Sachin', 'age':21},
            {'roll_no': 1006, 'name': 'Michel', 'age':22},
            {'roll_no': 1004, 'name': 'Mike', 'age':23},
            {'roll_no': 1005, 'name': 'Joseph', 'age':25},
        ]
        
        for data in dataset:
            existing_student = Student.objects.filter(roll_no=data['roll_no']).first()
            if existing_student:
                self.stdout.write(self.style.WARNING(f"Student with roll_no {data['roll_no']} already exists. Skipping insertion."))
            else:
                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
                self.stdout.write(self.style.SUCCESS(f"Inserted student: {data['name']} with roll_no {data['roll_no']}"))