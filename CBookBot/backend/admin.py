from django.contrib import admin

from .models import Book, BotUser, Tag, Author, BookTag


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'username']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class BookTagInlineAdmin(admin.TabularInline):
    model = BookTag
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price']
    inlines = [BookTagInlineAdmin]
