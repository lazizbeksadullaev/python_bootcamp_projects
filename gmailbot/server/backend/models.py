"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""
"""
/// 156 training H. Django Models #8
from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return f'{self.name}'
    class Meta:
        abstract = True


class Product(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True
"""
"""from django.db import models


class BotUser(models.Model):

    chat_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    bot_state = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.first_name}'
    def get_full_name(self):
        return f'{self.first_name}+{self.last_name}'

    class Meta:
        abstract = True


class Category(models.Model):

    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True

from django.db import models
from django.contrib.auth.models import User
class Problem(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True)
    class Difficulty(models.IntegerChoices):
        EASY = 1, 'Easy'
        MEDIUM = 2, 'Medium'
        HARD = 3, 'Hard'
        
    class Difficulty(models.IntegerChoices):
        EASY = 1
        MEDIUM = 2
        HARD = 3

    difficulty = models.IntegerField(choices=Difficulty.choices)

#Problem.Difficulty.labels # EASY lani olib baradi
#Problem.Difficulty.values # 1, 2, 3 lani olib beradi
#Problem.Difficulty.choices # (EASY, 1), (MEDIUM, 2)


"""
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User


class Problem(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=255)
    body = models.TextField(null=True)
    rating = models.FloatField(default=0)

    class Difficulty(models.IntegerChoices):
        EASY = 1
        MEDIUM = 2
        HARD = 3

    difficulty = models.IntegerField(choices=Difficulty.choices)


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    source_code= models.TextField()
    verdict = models.IntegerField(default=-2)

class Contest(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    problems = models.ManyToManyField(Problem)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()

'''
from django.db.models import Model, QuerySet


def get_problems(Problem: Model) -> QuerySet:
    all_entries = Problem.objects.filter(rating__gt = 4)

    return all_entries

/// 162 F6
from django.db.models import Model, QuerySet, Q


def get_problems(Problem: Model) -> QuerySet:
    all_entries = Problem.objects.filter(~Q(rating__range = (2.0, 4.0)) | Q(difficulty = 2))

    return all_entries    

'''


class Problem(models.Model):
    class Difficulty(models.IntegerChoices):
        EASY = 1
        MEDIUM = 2
        HARD = 3

    title = models.CharField(max_length=255)
    body = models.TextField(null=True)
    difficulty = models.IntegerField(choices=Difficulty.choices)
    rating = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}. {self.title}'

'''
/// F6 162
from django.db.models import Model, QuerySet, Q


def get_problems(Problem: Model) -> QuerySet:
    all_entries = Problem.objects.filter(~Q(rating__range=(2.0, 4.0))).order_by('-id')

    return all_entries[0]
/// F7 
from django.db.models import Model


def get_problems_count(Problem: Model) -> int:
    k = Problem.objects.all().order_by('rating').distinct('rating').count()
    return k
    
/// H8
from django.db.models import Model, QuerySet


def get_problems(Problem: Model) -> QuerySet:
   all_entries = Problem.objects.filter(rating__in=[1.0, 2.0, 3.0, 4.0, 5.0]).order_by('difficulty')

   return all_entries

/// I9
from django.db.models import Model, QuerySet


def get_problems(Problem: Model) -> QuerySet:
   all_entries = Problem.objects.filter(title__startswith='A')

   return all_entries
   
/// J
from django.db.models import Model, QuerySet, Max


def get_problems(Problem: Model) -> QuerySet:
    max_rating = Problem.objects.aggregate(max_rating=Max('rating'))['max_rating']
    # aggregate(a=b) 1 ta eltdan iborat {'a':...} dict qaytaradi
    all_entries = Problem.objects.filter(rating=max_rating)
    return all_entries
/// G7
from django.db.models import Model


def get_problems_count(Problem: Model) -> int:
    k = Problem.objects.all().order_by('rating').distinct('rating').count()
    return k

///  K11
from django.db.models import Model, QuerySet, functions, Max


def get_problems(Problem: Model) -> QuerySet:
    problems = Problem.objects.all().annotate(

        body_length = functions.Length('body')
    )
    max_length = problems.aggregate(max_length=Max('body_length'))['max_length']
    return problems.filter(body_length=max_length)

/// M2
from django.db.models import Model, QuerySet

def get_languages(ProgrammingLanguage: Model) -> QuerySet:
    all_entries = ProgrammingLanguage.languages.filter(name='Python')
    return all_entries

///

'''
from django.db.models import Model, QuerySet, Q


def get_languages(ProgrammingLanguage: Model) -> QuerySet:
   
   all_entries = ProgrammingLanguage.languages.filter(Q(name='Python') | Q(name='C++'))
   
   return all_entries
 
 

