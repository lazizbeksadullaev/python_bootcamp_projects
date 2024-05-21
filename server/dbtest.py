"""

print(Employee.employees.first())
print(Department.departments.first())
print(Employee.male_employees.values_list('gender', 'first_name'))
print(Employee.male_employees.first())

print('if when thenlani ishlatish\n')
e = Employee.employees.annotate(name=Case(
    When(Q(age__lt=18), then=functions.Lower('first_name')),
    When(Q(age__lt=30), then=functions.Upper('first_name')),
    default=F('first_name'),
)).values_list('age', 'first_name', 'name')

for obj in e[:20]:
    print(obj)

print('\nsof SQL ni o`zina murojaat qilish va so`rovla yozish\n')
print(Employee.employees.extra(where=['age<20'])[:8])
#print(Employee.employees.raw('SELECT * FROM backend(in general my_app_... buladi bu backendni urnida)_employee')[:10])
print(Employee.employees.raw('SELECT * FROM backend_employee WHERE id BETWEEN 3 AND 20')[:5])

print('\nrandom sanalani yaratish\n')

import random
from django.utils import timezone



seconds = 12*365*24*60*60
for e in Employee.employees.all():
    dt = timezone.now()
    dt -= timezone.timedelta(seconds=random.randint(0, seconds))
    e.created = dt
    e.save()


"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from backend.models import Employee, Department
from django.db.models import F, Q, Case, When, functions
from django.db import models
from django.db.models import QuerySet



def get_university(Employee: models.Model) -> QuerySet:
    length = Employee.employees.all().annotate(
        name_length = functions.Length('first_name')
    )
    all_employees = length.filter(name_length__range=(10, 20)).last()

    return all_employees

from django.db.models import QuerySet


def get_students(Employee: models.Model) -> QuerySet:
    even_ages = Employee.employees.all()
    even_ages = even_ages.delete()
    for e in Employee.employees.values_list('age')[0]:
        if e%2 == 0:
            even_ages +=     
    return even_ages

print(get_university(Employee))
print(get_students(Employee))