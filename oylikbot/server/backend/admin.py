from django.contrib import admin
from .models import Employee
from .models import ProgrammingLanguage
from .models import Department
from .models import Employee


# Register your models here.

'''@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ['languages', 'name']
@admin.register(SalaryData)
class SalaryDataAdmin(admin.ModelAdmin):
    list_display = ['month']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'phone_number']'''