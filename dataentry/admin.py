from django.contrib import admin
from .models import Student, Customer, Upload, Employee
# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'age')
    search_fields = ('roll_no', 'name')
    list_filter = ('age',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'country')
    search_fields = ('customer_name', 'country')
    list_filter = ('country',)

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'file', 'uploaded_at')
    search_fields = ('model_name',)
    list_filter = ('uploaded_at',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'employee_name', 'designation', 'salary', 'retirement', 'other_benefits', 'total_benefits', 'total_compensation')
    search_fields = ('employee_id', 'employee_name', 'designation')
    list_filter = ('designation',)

