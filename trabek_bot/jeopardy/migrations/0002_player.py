# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeopardy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('score', models.IntegerField(default=0)),
                ('asked', models.IntegerField(default=0)),
                ('right_questions', models.ManyToManyField(related_name='question_id_right', to='jeopardy.Question')),
                ('wrong_questions', models.ManyToManyField(related_name='question_id_wrong', to='jeopardy.Question')),
            ],
        ),
    ]
