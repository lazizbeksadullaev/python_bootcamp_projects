# Generated by Django 3.2 on 2021-05-29 15:25

import app.models
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField(unique=True)),
                ('full_name', models.CharField(max_length=250)),
                ('balls', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('User', 'User'), ('Group', 'Group'), ('Admin', 'Admin')], default='User', max_length=10)),
                ('bot_state', models.CharField(blank=True, max_length=50, null=True)),
                ('lang', models.CharField(choices=[('uz', 'Uz'), ('ru', 'Ru')], default='uz', max_length=10)),
                ('problem_choiced_id', models.IntegerField(default=1)),
                ('project_choiced_id', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-balls'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Single', 'Single'), ('Multi', 'Multi')], max_length=10)),
                ('title_uz', models.TextField(verbose_name='Savol')),
                ('title_ru', models.TextField(verbose_name='Вопрос')),
                ('options_uz', models.TextField(verbose_name='Variantlar')),
                ('options_ru', models.TextField(verbose_name='Варианты')),
                ('answers_uz', models.TextField(verbose_name='Javoblar')),
                ('answers_ru', models.TextField(verbose_name='Ответы')),
                ('image', models.ImageField(default='cpython/tests/default.png', upload_to=app.models.question_image_directory_path)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['updated'],
            },
            managers=[
                ('questions', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('Key', 'Key'), ('Message', 'Message'), ('Smile', 'Smile')], max_length=10)),
                ('body_uz', models.TextField()),
                ('body_ru', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('templates', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('duration', models.TimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('tests', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TestOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_ones', to='app.test')),
            ],
            options={
                'unique_together': {('test', 'number')},
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_results', to='app.botuser')),
            ],
            managers=[
                ('results', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TestResultOne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=255)),
                ('test_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.testone')),
                ('test_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_result_ones', to='app.testresult')),
            ],
        ),
    ]
