import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from backend.models import Employee, ProgrammingLanguage, Department
from django.db.models import Q, F, functions

'''
from backend.models import Employee
from django.db.models import F, Q, Case, When, functions

e = Employee.employees.annotate(name=Case(
    When(Q(age__lt=18), then=functions.Lower('first_name')),
    When(Q(age__lt=30), then=functions.Upper('first_name')),
    default=F('first_name'),
)).values_list('age', 'first_name', 'name')


import random
from django.utils import timezone


seconds = 12*365*24*60*60
for e in Employee.employees.all():
    dt = timezone.now()
    dt -= timezone.timedelta(seconds=random.randint(0, seconds))
    e.created = dt
    e.save()

e = Employee.employees.annotate(bonus=Case(
    When(created__gt=timezone.now()-timezone.timedelta(days=365), then=5),
    When(created__gt=timezone.now()-timezone.timedelta(days=2*365), then=10),
    When(created__gt=timezone.now()-timezone.timedelta(days=5*365), then=15),
    default=25,
))

for obj in e.values_list('created', 'bonus')[:20]:
    print(obj[0].strftime('%d/%m/%Y'), obj[1])

print(Employee.employees.extra(where=['age < 20'])[:10])
print(Employee.employees.raw('SELECT * FROM backend_employee')[:10])
'''



Employee.employees.all() # SELECT * FROM backend_employee
Employee.employees.all().values_list('age', 'first_name')  # SELECT age, first_name FROM backend_employee
Employee.employees.all().values_list('age', flat=True)  # SELECT age FROM backend_employee

Employee.employees.filter(age=10)  # SELECT * FROM backend_employee WHERE age=10
# age=10 => age__exact=10
# field_name__lookup_name

# lt, gte, lte, gt, ne, exact, startswith, endswith, contains, range, in, day, month, date, year
# created__day=10


Employee.employees.exclude(age__range=[10, 20])  # WHERE age NOT BETWEEN (10, 20)
Employee.employees.filter(age=10, first_name__startswith='A')  # WHERE age=10 AND first_name LIKE 'A%'

# starswith LIKE 'A%'
# endswith LIKE '%A'
# contains LIKE '%A%'


# icontains='abc' => ABC, Abc, abc


first_language = ProgrammingLanguage.languages.first()
last_language = ProgrammingLanguage.languages.last()
print(first_language)
print(last_language)

print(first_language.id)
Employee.employees.filter(language=first_language)  # SELECT * FROM backend_employee WHERE language_id=4

Employee.employees.filter(language__name='Python')
