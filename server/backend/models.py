from math import floor
from tkinter.tix import MAX
from django.db import models
from django.db.models import functions, Q


class ProgrammingLanguage(models.Model):
    languages = models.Manager()
    name = models.CharField(max_length=255)

def __str__(self):
        return self.name


class Department(models.Model):
    departments = models.Manager()
    name = models.CharField(max_length=255)
    floor = models.PositiveIntegerField()
    class Meta:
        constraints=[models.CheckConstraint(
            check=Q(floor__lt=100),
            name='Xorazmda 100 qavatli bino nishidi'
        )]


    def __str__(self):
        return self.name

class MaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gender=1)
    
class Employee(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 1
        FEMALE = 2

    employees = models.Manager()
    male_employees=MaleManager()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.IntegerField(choices=Gender.choices)
    department = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    language = models.ForeignKey(
        to=ProgrammingLanguage,
        on_delete=models.CASCADE,
        related_name='employees',
    )

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        return self.get_full_name()
    class Meta:
        constraints = [models.CheckConstraint(
            check=Q(age__lt=100),
            name='Yosh juda katta bo`ldi'
        )]

#####
from django.db.models import Model, QuerySet, functions, Max


def get_languages(ProgrammingLanguage: Model) -> QuerySet:
   name_length_set = ProgrammingLanguage.languages.all().annotate(
       name_length = functions.Length('name')
   )#bu yerda anotate 'name' ustuni uzunlikidan iborat name_length nomli yangi ustun yaratadi
   #va bu ustun faqat manashu annotate surovi ichida mavjud bb turadi, shunin uchn bu anotate 
   # surovidan galgan query setni bir uzgaruvchiga saqlash garak. Men hozr name_length uzgaruvchida 
   # anotate surovidan qaytgan query setni saqlab qo`yamiz.

   max_length_name = name_length_set.aggregate(max_length=Max('name_length'))['max_length']
   
   return name_length_set.filter(name_length=max_length_name)
   #return ProgrammingLanguage.languages.filter('name_length'=max_length_name)