# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 09:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='owner',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['abbreviation'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-published_at']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='blog',
        ),
        migrations.AddField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
    ]
