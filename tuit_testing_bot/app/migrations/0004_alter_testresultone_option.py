# Generated by Django 3.2 on 2021-05-30 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210530_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresultone',
            name='option',
            field=models.CharField(default='', max_length=255),
        ),
    ]
