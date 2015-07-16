# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(editable=False)),
                ('score', models.IntegerField(verbose_name='Rating')),
                ('content', models.TextField(verbose_name='Review')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(related_name='reviews', editable=False, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='reviews', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_added',),
                'verbose_name': 'reviewed item',
                'verbose_name_plural': 'reviewed items',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like', models.BooleanField(default=True)),
                ('ip_address', models.IPAddressField(blank=True)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now, verbose_name='date added', editable=False)),
                ('date_changed', models.DateTimeField(default=datetime.datetime.now, verbose_name='date changed', editable=False)),
                ('review', models.ForeignKey(related_name='reviews_votes', verbose_name='review', to='reviews.ReviewedItem')),
                ('user', models.ForeignKey(related_name='reviews_votes', verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
        ),
    ]
