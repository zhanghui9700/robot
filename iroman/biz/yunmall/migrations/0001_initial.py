# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('delete_date', models.DateTimeField(null=True, blank=True)),
                ('code', models.CharField(max_length=128, unique=True, null=True)),
                ('username', models.CharField(max_length=128, verbose_name='Name')),
                ('mobile', models.CharField(max_length=32, verbose_name='Mobile')),
                ('password', models.CharField(max_length=32, verbose_name='Password')),
                ('pay_password', models.CharField(max_length=32, null=True, verbose_name='Pay Password')),
                ('child_count', models.IntegerField(default=0, verbose_name='Child')),
                ('nickname', models.CharField(max_length=128, null=True, verbose_name='Chinese Name')),
                ('id_card', models.CharField(max_length=128, null=True, verbose_name='Chinese ID')),
                ('email', models.EmailField(max_length=128, null=True, verbose_name='Email')),
                ('step', models.IntegerField(default=1, verbose_name='Process', choices=[(0, 'Error'), (1, 'Register'), (2, 'Profile'), (3, 'Pay Password'), (99, 'Succeed')])),
                ('parent', models.ForeignKey(db_constraint=False, blank=True, to='yunmall.Fish', null=True)),
            ],
            options={
                'db_table': 'yunmall_fish',
                'verbose_name': 'Fish',
                'verbose_name_plural': 'Fishes',
            },
            bases=(models.Model,),
        ),
    ]
