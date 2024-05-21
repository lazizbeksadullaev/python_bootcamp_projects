from django.db import models

# Create your models here.
class ProgrammingLanguage(models.Model):
    languages = models.Manager()
    name = models.CharField(max_length=255)


class Department(models.Model):
    deparments = models.Manager()
    name = models.CharField(max_length=255)
    floor = models.PositiveIntegerField()


class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = 1
        FEMALE = 2

    employees = models.Manager()
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