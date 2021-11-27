from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_not_empty

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Группа, к которой будет относиться пост'
    )
    slug = models.SlugField(
        max_length=100, unique=True,
        verbose_name='Слаг',
        help_text='Слаг, по которому можно найти группу'
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Тематика группы'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    text = models.TextField(
        validators=[validate_not_empty],
        verbose_name='Текст поста',
        help_text='Текст поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата, когда был опубликован пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста',
        help_text='Автор поста'
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
