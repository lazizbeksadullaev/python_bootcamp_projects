# Generated by Django 4.0.4 on 2022-04-26 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_employee_languages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='languages',
        ),
    ]
