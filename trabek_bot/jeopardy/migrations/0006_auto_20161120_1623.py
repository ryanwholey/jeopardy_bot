# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0005_auto_20161120_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='air_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
