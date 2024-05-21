import random

from django.db import models
from django.db.models import ObjectDoesNotExist
from django.utils import timezone


class CustomManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='User')


class GroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Group')


class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Admin')


class BotUser(models.Model):
    class Lang(models.TextChoices):
        UZ = 'uz'
        RU = 'ru'

    class Type(models.TextChoices):
        USER = 'User'
        GROUP = 'Group'
        ADMIN = 'Admin'

    objects = CustomManager()
    users = UserManager()
    groups = GroupManager()
    admins = AdminManager()

    chat_id = models.IntegerField(unique=True)
    full_name = models.CharField(max_length=250)
    balls = models.IntegerField(default=0)
    type = models.CharField(
        max_length=10,
        default=Type.USER,
        choices=Type.choices
    )
    bot_state = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    lang = models.CharField(
        max_length=10,
        choices=Lang.choices,
        default=Lang.UZ,
    )
    problem_choiced_id = models.IntegerField(default=1)
    project_choiced_id = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-balls']

    def __str__(self):
        return self.full_name


def question_image_directory_path(instance, filename):
    return f'app/tests/{instance.id}.jpg'


class Question(models.Model):
    class Type(models.TextChoices):
        SINGLE = 'Single'
        MULTI = 'Multi'

    DEFAULT_IMAGE = 'tests/default.png'
    questions = models.Manager()
    type = models.CharField(max_length=10, choices=Type.choices)
    title_uz = models.TextField(verbose_name='Savol')
    title_ru = models.TextField(verbose_name='Вопрос')
    options_uz = models.TextField(verbose_name='Variantlar')
    options_ru = models.TextField(verbose_name='Варианты')
    answers_uz = models.TextField(verbose_name='Javoblar')
    answers_ru = models.TextField(verbose_name='Ответы')
    image = models.ImageField(
        default=DEFAULT_IMAGE,
        upload_to=question_image_directory_path,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_title(self, lang):
        if lang == BotUser.Lang.UZ:
            return self.title_uz
        elif lang == BotUser.Lang.RU:
            return self.title_ru

    def get_options(self, lang):
        options = getattr(self, f'options_{lang}')
        options_list = list(map(lambda s: s.strip('\r'), options.split('\n')))
        return options_list

    def get_answers(self, lang):
        answers = getattr(self, f'answers_{lang}')
        answers_list = list(map(lambda s: s.strip('\r'), answers.split('\n')))
        return answers_list

    def check_answers(self, user_answers_list: list[str]):
        sorted_user_answers_list = sorted(user_answers_list)
        answers_uz_list = self.get_answers(BotUser.Lang.UZ)
        answers_ru_list = self.get_answers(BotUser.Lang.RU)
        for answers_list in [answers_uz_list, answers_ru_list]:
            sorted_answers_list = sorted(list(answers_list))
            if sorted_answers_list == sorted_user_answers_list:
                return True

        return False

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        options = self.options_uz.split('\n')
        random.shuffle(options)
        self.options_uz = '\n'.join(options)
        options = self.options_ru.split('\n')
        random.shuffle(options)
        self.options_ru = '\n'.join(options)
        result = super().save(*args, **kwargs)
        return result

    class Meta:
        ordering = ['updated']


class Test(models.Model):
    tests = models.Manager()
    title = models.CharField(max_length=255)
    duration = models.TimeField()
    questions_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def all_questions_count(self):
        return self.test_ones.all().count()

    def __str__(self):
        return self.title


class TestOne(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='test_ones'
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['test__id', 'number']
        unique_together = [('test', 'number')]

    def __str__(self):
        return f'{self.test} - {self.number}'


class TestResult(models.Model):
    results = models.Manager()
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE,
        related_name='test_results'
    )
    solved = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def remaining_time(self):
        passed_seconds = int((timezone.now() - self.created).total_seconds())
        duration = self.test.duration
        seconds = duration.hour*3600 + duration.minute*60 + duration.second
        remaining_seconds = seconds - passed_seconds
        return remaining_seconds

    @property
    def finished(self):
        return self.remaining_time <= 0

    def __str__(self):
        return f'{self.user} - {self.test} ({self.solved})'


class TestResultOne(models.Model):
    test_result = models.ForeignKey(
        TestResult,
        on_delete=models.CASCADE,
        related_name='test_result_ones',
    )
    test_one = models.ForeignKey(TestOne, on_delete=models.CASCADE)
    option = models.CharField(max_length=255, default='')


class KeyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Key')


class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Message')


class SmileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Smile')


class Template(models.Model):
    class Type(models.TextChoices):
        KEY = 'Key'
        MESSAGE = 'Message'
        SMILE = 'Smile'

    templates = models.Manager()
    keys = KeyManager()
    messages = MessageManager()
    smiles = SmileManager()
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type.choices)
    body_uz = models.TextField()
    body_ru = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)

        keys = Template.keys.all()
        messages = Template.messages.all()
        smiles = Template.smiles.all()
        with open('app/templates.py', 'w') as file:
            file.write('from .models import Template\n\n')
            file.write('\n')
            file.write('keys = Template.keys.all()\n')
            file.write('messages = Template.messages.all()\n\n')
            file.write('smiles = Template.smiles.all()\n\n')
            file.write('\n')
            file.write('class Keys():\n')
            for index, key in enumerate(keys):
                file.write(f'    {key.title} = keys[{index}]\n')

            file.write('\n\n')
            file.write('class Messages():\n')
            for index, message in enumerate(messages):
                file.write(f'    {message.title} = messages[{index}]\n')

            file.write('\n\n')
            file.write('class Smiles():\n')
            for index, smile in enumerate(smiles):
                file.write(f'    {smile.title} = smiles[{index}]\n')

        return result

    @property
    def text(self):
        return self.body_uz

    def get(self, lang):
        if lang == BotUser.Lang.UZ:
            return self.body_uz
        elif lang == BotUser.Lang.RU:
            return self.body_ru

    def getall(self):
        return (self.body_uz, self.body_ru)

    def format(self, **kwargs):
        return self.body_uz.format(**kwargs)

    def __format__(self, format_spec):
        return format(self.body_uz, format_spec)

    def __str__(self):
        return self.title
