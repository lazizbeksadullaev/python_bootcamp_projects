from tokenize import group
from typing import Set
from django.db import models
'''
# Django contest 27.04.2022

/// A1
class University(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    class Meta:
        abstract = True

/// A2
from django.db import models


class Rector(models.Model):
    
    full_name = models.CharField(max_length=255)
    date_of_birthday = models.CharField(max_length=255)

    class Meta:
        abstract = True



class University(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    rector = models.ForeignKey(Rector, related_name='university', null=True, on_delete=models.SET)
    class Meta:
        abstract = True

/// B2
from django.db import models
from django.db.models import QuerySet


def get_universities(University: models.Model) -> QuerySet:
    all_universities = University.universities.filter(country_name__startswith='uz')
    
    return all_universities

/// B3

class University(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    rector = models.OneToOneField(to=Rector, related_name='university', null=True, on_delete=models.SET_NULL)
    class Meta:
        abstract = True

from django.db import models
from django.db.models import QuerySet, functions, Q, F


def get_university(University: models.Model) -> QuerySet:
    length = University.universities.all().annotate(
        name_length = functions.Length('name')
    )
    all_universities = length.filter(name_length__range=(10, 20)).values_list('name', 'name_length').last()[0]
    return all_universities

/// C1
from django.db import models
from django.db.models import QuerySet


def get_universities(University: models.Model) -> QuerySet:
    all_notempty_rectors = University.universities.exclude(rector__isnull=True)
    return all_notempty_rectors

/// C2
from django.db import models
from django.db.models import QuerySet


def get_rectors(Rector: models.Model) -> QuerySet:
    all_rectors = Rector.objects.filter(date_of_birthday.year=1980)
    return all_rectors

/// D1
from django.db.models import QuerySet


def get_students(universitet) -> QuerySet:
    related_students = universitet.students.all()
    return related_students

///

'''
from django.db import models


class Rector(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birthday = models.DateField()
    class Meta:
        abstract = True


class University(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)
    rector = models.OneToOneField(to=Rector, related_name='university', null=True, on_delete=models.SET_NULL)
    class Meta:
        abstract = True

class Student(models.Model):
    class Group(models.IntegerChoices):
        BIR =1
        IKKI = 2
        UCH = 3
        TURT = 4
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    group_number = models.PositiveIntegerField(choices=Group.choices)
    university = models.ForeignKey(University, related_name='students', on_delete=models.CASCADE)

    class Meta:
        abstract = True

from django.db import models
from django.db.models import QuerySet, F


def get_students(Student: models.Model) -> QuerySet:
    even_groups = Student.students.annotate(
        x = F('group_number')%2
    )
    return even_groups.filter(x=0)