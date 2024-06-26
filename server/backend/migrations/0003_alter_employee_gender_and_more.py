# Generated by Django 4.0.3 on 2022-04-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_alter_department_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female')]),
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.CheckConstraint(check=models.Q(('floor__gt', 0)), name='Department manfiy qavatda bo`lmidi'),
        ),
    ]
