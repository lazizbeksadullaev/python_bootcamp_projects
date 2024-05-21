"""from telebot import TeleBot
#from task_2 import TOKEN

TOKEN = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'

bot = TeleBot(TOKEN, parse_mode='HTML')

@bot.message_handler()
/// A
def prime(n):
    i = 2
    k = 0
    while True:
        t = True
        for j in range(2, i):
            if i % j == 0:
                t = False
        if t:
            k += 1
            yield i
        i += 1
        if k == n:
            return

n = int(input())

for i in prime(n):
    print(i)
// B
n = int(input())
matrix = list()
for i in range(n):
    row=[]
    for j in range(n):
        row.append(int(input()))
    matrix.append(row)

print(matrix)

/// J2
from django.db import models
from django.contrib.auth.models import User

class ProblemManager(models.Manager):
    class Meta:
        abstract = True
    def get_queryset(self):
        return super().get_queryset().filter(verdict = 1)

class AttemptManager(models.Manager):
    class Meta:
        abstract = True
    def get_queryset(self):
        return super().get_queryset()


class Problem(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True)
    difficulty = models.IntegerField()
    rating = models.FloatField(default=0)

    class Meta:
        abstract = True


class Attempt(models.Model):

    attempts = AttemptManager()
    adopted = ProblemManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    source_code = models.TextField()
    verdict = models.IntegerField(default=-2)
    #created = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True


class CustomManager(models.Manager):
    def get_or_none(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except Exception:
            return None


class PythonistsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(language__name='Python')


class YoungManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(age__lt=18)
/// J2

from django.db import models
from django.contrib.auth.models import User

class ProblemManager(models.Manager):
    class Meta:
        abstract = True
    def get_queryset(self):
        return super().get_queryset().filter(verdict = 1)

class AttemptManager(models.Manager):
    class Meta:
        abstract = True
    def get_queryset(self):
        return super().get_queryset()


class Problem(models.Model):
    #problem = models.Manager.get_queryset()
    title = models.CharField(max_length=255)
    body = models.TextField(null=True)
    difficulty = models.IntegerField()
    rating = models.FloatField(default=0)

    class Meta:
        abstract = True


class Attempt(models.Model):

    attempts = models.Manager()
    adopted = models.Manager().get_queryset().filter(verdict=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    source_code = models.TextField()
    verdict = models.IntegerField(default=-2)
    #created = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        abstract = True


/// J3
from django.db.models import Model, QuerySet


def get_problems(Problem: Model) -> QuerySet:
   return Problem.objects.filter(rating__in =[1.0, 2.0, 3.0, 4.0, 5.0]).order_by('difficulty')

/// K2
def get_problems(Problem): return Problem.objects.all().annotate(id_last=__import__('django').db.models.F('id')%10).filter(id_last__in=[2,3,5,7])
yoki
def get_problems(Problem): return Problem.objects.all().annotate(id_last=__import__('django').db.models.F('id')%10).filter(id_last__in=[2,3,5,7])

"""
def check_three_matrix(a: list):
    s = 0
    for i in range(3):
        for j in range(3):
            s += a[i][j]
    
    return s == 45
'''
def row__col_matrix(a: list):
    return sum(a) == 45

for i in range(9):
    for j in range(9):
        if a[i][j] == 0:
            x = i
            y = j
#a[x].remove(0)
'''
a = [list(map(int, input().split())) for _ in range(9)]
checked = True
for i in range(9):
    if sum(a[i]) != 45 and a[i][0] != 45:
        checked = False
        break
three_matrix = list()
for i in range(0, 9):
    three_matrix.append()
        

raqamlar ={0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
print(*raqamlar-set(a[x]))



