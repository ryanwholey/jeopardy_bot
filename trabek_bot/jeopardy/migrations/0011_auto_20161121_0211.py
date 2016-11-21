# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0010_auto_20161121_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='right_questions',
            field=models.ManyToManyField(related_name='question_id_right', to='jeopardy.Question', blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='wrong_questions',
            field=models.ManyToManyField(related_name='question_id_wrong', to='jeopardy.Question', blank=True),
        ),
    ]
