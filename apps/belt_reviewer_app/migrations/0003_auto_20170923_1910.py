# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 02:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_reviewer_app', '0002_author_book_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='Author_id',
            new_name='Author',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='User_id',
            new_name='User',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='Book_id',
            new_name='Book',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='User_id',
            new_name='User',
        ),
    ]
