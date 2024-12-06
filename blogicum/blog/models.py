"""Модели проекта"""
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from blog.constants import MAX_LENGTH_TITLE


User = get_user_model()


class Category(models.Model):
    """Модель категории"""
    title = models.CharField('Заголовок', max_length=MAX_LENGTH_TITLE)
    description = models.TextField('Описание')
    image = models.ImageField('Фото', upload_to='post_images', blank=True)
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(models.Model):
    """Модель локации"""
    name = models.CharField('Название места', max_length=MAX_LENGTH_TITLE)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель поста"""
    title = models.CharField('Заголовок', max_length=MAX_LENGTH_TITLE)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        related_name='posts',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        related_name='posts',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    image = models.ImageField('Фото', upload_to='blog_image', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse("blog:profile", args=[self.author])
    
    def comment_count(self):
        return self.comments.count()
    

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель комментария"""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', null=True
    )
    text = models.TextField('Комментарии к записи')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return (self.text)
    

class Profile(models.Model):
    """Модель профиля"""
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
