from django.db import models
from pytils.translit import slugify


class BaseCatalog(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(verbose_name='SLUG', null=True,
                            blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Genre(BaseCatalog):
    class Meta:
        ordering = ('pk',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(BaseCatalog):
    class Meta:
        ordering = ('pk',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        null=True, blank=True,
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='titles')
    description = models.TextField(null=True, blank=True)

    def genres(self):  # method for admin list_display
        return ', '.join([obj.name for obj in self.genre.all()])

    def __str__(self):
        return f'{self.name} ({self.year}г.)'

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
