# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 01:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_reviewer_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('Author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='belt_reviewer_app.Author')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='belt_reviewer_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('rating', models.IntegerField(default=0)),
                ('Book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='belt_reviewer_app.Book')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='belt_reviewer_app.User')),
            ],
        ),
    ]
