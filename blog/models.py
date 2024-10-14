from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}
class Blog(models.Model):

    title = models.CharField(max_length=150, verbose_name='Заголовок', help_text='Введите заголовок статьи')
    body = models.TextField(verbose_name='Содержимое', help_text='Введите основной текст публикации')
    preview = models.ImageField(upload_to='blog/images', verbose_name='Изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    author = models.ForeignKey(
        User,
        verbose_name="автор",
        help_text='Укажите автора',
        on_delete=models.SET_NULL,
        **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)  # Сортировка по дате создания в обратном порядке