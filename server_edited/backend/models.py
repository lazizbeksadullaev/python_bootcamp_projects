import random

from django.db import models
from django.contrib import admin
from django.utils.html import format_html


class ProgrammingLanguage(models.Model):
    languages = models.Manager()
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CustomManager(models.Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except Exception:
            return None


class Department(models.Model):
    departments = CustomManager()
    name = models.CharField(max_length=255)
    floor = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class PythonistsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(language__name='Python')


class YoungManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(age__lt=18)


class Employee(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 1
        FEMALE = 2

    employees = models.Manager()
    pythonists = PythonistsManager()
    young = YoungManager()

    first_name = models.CharField(max_length=255,
                                  verbose_name='Ismi')
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
    created = models.DateTimeField(auto_now_add=True)

    @admin.display(description='To`liq nomi')
    def get_full_name_html(self):
        full_name = ' '.join([self.first_name, self.last_name])
        colors = ['red', 'green', 'blue']
        html = str()
        for c in full_name:
            color = random.choice(colors)
            html += f'<b style="color: {color};">{c}</b>'

        return format_html(html)

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def __str__(self):
        return self.get_full_name()
