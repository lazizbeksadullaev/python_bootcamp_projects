import os

from django.db import models
from django.db.models import functions, Q


class BotUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=255,
                                  verbose_name='Ismi')
    last_name = models.CharField(max_length=255,
                                 verbose_name='Familyasi',
                                 null=True)
    username = models.CharField(max_length=255,
                                unique=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = verbose_name + 'lar'
        constraints = [models.UniqueConstraint(
            functions.Lower('username'),
            name='Usernameni tekshirish'
        )]


class Tag(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Nomi')

    class Meta:
        verbose_name = 'Teg'
        verbose_name_plural = verbose_name + 'lar'

    def __str__(self):
        return self.name


class Author(models.Model):
    full_name = models.CharField(max_length=255,
                                 verbose_name='To`liq ismi')

    class Meta:
        verbose_name = 'Muallif'
        verbose_name_plural = verbose_name + 'lar'


def book_image_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = instance.title + '.' + extension
    return os.path.join('book_images', filename)


class Book(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Nomi')
    description = models.TextField(verbose_name='Sharxi')
    price = models.FloatField(verbose_name='Narxi')
    image = models.ImageField(upload_to=book_image_directory_path,
                              verbose_name='Rasm')

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = verbose_name + 'lar'
        constraints = [models.CheckConstraint(
            check = Q(price__lt = 10000),
            name = 'Katta summa kiritilgan'
        )]


class BookTag(models.Model):
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='tags',
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
