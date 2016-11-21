# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0004_auto_20161120_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='right_questions',
            field=models.ManyToManyField(related_name='question_id_right', to='jeopardy.Question'),
        ),
        migrations.AlterField(
            model_name='player',
            name='wrong_questions',
            field=models.ManyToManyField(related_name='question_id_wrong', to='jeopardy.Question'),
        ),
    ]
