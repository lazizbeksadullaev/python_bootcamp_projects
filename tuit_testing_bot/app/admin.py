from django.contrib import admin

from .models import (BotUser, Question, Template, Test, TestOne,
                     TestResult, TestResultOne)


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'chat_id', 'balls', 'bot_state', 'created']
    search_fields = ['full_name']
    actions = ['reset_bot_state', 'rating_update']

    @admin.action(description='Сбросить состояние')
    def reset_bot_state(self, request, queryset):
        queryset.update(bot_state=None)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_per_page = 250
    list_display = ['id', 'title', 'type']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_uz', 'type']
    search_fields = ['title_uz', 'title_ru']


class TestOneAdminInline(admin.TabularInline):
    model = TestOne
    extra = 1
    max_num = 10


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'duration', 'questions_count',
                    'all_questions_count']
    inlines = [TestOneAdminInline]


@admin.register(TestResult)
class TestResultsAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'solved', 'finished']


@admin.register(TestResultOne)
class TestResultsOneAdmin(admin.ModelAdmin):
    list_display = ['test_result', 'test_one', 'option']
