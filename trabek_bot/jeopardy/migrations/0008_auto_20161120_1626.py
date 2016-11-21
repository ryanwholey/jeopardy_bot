# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0007_auto_20161120_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='show',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
