from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PublishTimeModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Category(PublishTimeModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
    )
    description = models.TextField(
        'Описание',
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, '
                   'цифры, дефис и подчёркивание.'),
    )

    class Meta:
        verbose_name = 'объект «Категория»'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishTimeModel):
    name = models.CharField(
        'Название места',
        max_length=256,
    )

    class Meta:
        verbose_name = 'объект «Местоположение»'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishTimeModel):
    title = models.CharField(
        'Заголовок',
        max_length=256,
    )
    text = models.TextField(
        'Текст',
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.'),
    )
    image = models.ImageField(
        'Изображение публикации',
        upload_to='posts_images',
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    class Meta:
        verbose_name = 'объект «Публикация»'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(
        'Текст комментария',
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments',
    )

    class Meta:
        verbose_name = 'объект «Комментарий»'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text
