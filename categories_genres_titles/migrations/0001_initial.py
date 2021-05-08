# Generated by Django 3.0.5 on 2021-05-01 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='SLUG')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('basecatalog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='categories_genres_titles.BaseCatalog')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('pk',),
            },
            bases=('categories_genres_titles.basecatalog',),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('basecatalog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='categories_genres_titles.BaseCatalog')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('pk',),
            },
            bases=('categories_genres_titles.basecatalog',),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Год')),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='categories_genres_titles.Category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(related_name='titles', to='categories_genres_titles.Genre', verbose_name='Жанры')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('pk',),
            },
        ),
    ]