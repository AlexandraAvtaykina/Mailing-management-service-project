from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое статьи')
    image = models.ImageField(upload_to='image/', verbose_name='изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    date_published = models.DateTimeField(verbose_name='дата публикации', **NULLABLE)
    
    def __str__(self):
        return f'{self.title} {self.views_count} {self.date_published}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ('title', 'date_published',)
