'''
///
#print('COMPUTER SIMULATION OF THE HEAT TRANSFER PROCESS IN REGENERATIVE HEAT EXCHANGERS'.lower())
def ekub(a,b):
    while a != 0 and b != 0:
        if a>b:
            a %= b
        else:
            b %= a

        ekub_q = a+b

    return ekub_q

print(ekub(60, 21))

///
'''
from django.contrib import admin

# Register your models here.
from .models import Problem, Attempt, Contest

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'difficulty']
@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'problem', 'source_code', 'verdict']
@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'start_time', 'finish_time']