# Generated by Django 4.0.3 on 2022-04-19 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_problem_created_problem_rating_problem_updated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attempt',
            name='created',
        ),
        migrations.RemoveField(
            model_name='attempt',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='created',
        ),
        migrations.RemoveField(
            model_name='contest',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='created',
        ),
        migrations.RemoveField(
            model_name='problem',
            name='updated',
        ),
    ]
