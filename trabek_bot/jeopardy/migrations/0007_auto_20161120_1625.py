# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0006_auto_20161120_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='air_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
