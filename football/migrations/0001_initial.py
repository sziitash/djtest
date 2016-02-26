# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoalNum',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, blank=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('groupname', models.CharField(max_length=50, blank=True)),
                ('goalnum', models.IntegerField(null=True, blank=True)),
                ('playcount', models.IntegerField(null=True, blank=True)),
                ('playtime', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'goal_num',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='football.Question'),
        ),
    ]
