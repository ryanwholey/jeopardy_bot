# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0008_auto_20161120_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='jeopardy_round',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
