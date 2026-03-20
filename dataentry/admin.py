from django.contrib import admin
from .models import Student, Customer, Upload
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

