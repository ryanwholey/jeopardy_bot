# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=255, db_index=True)),
                ('air_date', models.DateTimeField(verbose_name=b'date aired')),
                ('question', models.TextField()),
                ('value', models.IntegerField()),
                ('answer', models.CharField(max_length=255)),
                ('jeopardy_round', models.CharField(max_length=255)),
                ('show', models.IntegerField()),
            ],
        ),
    ]
