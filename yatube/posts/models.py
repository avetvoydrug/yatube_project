from typing import Any
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста',
                            help_text='Введите текст поста')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name= 'posts'
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='posts',
        help_text='Выберите тематическую группу '
                  'в выпадающем списке по желанию'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


    
# Create your models here.
