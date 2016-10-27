# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yunmall', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcceedCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('delete_date', models.DateTimeField(null=True, blank=True)),
                ('code', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'db_table': 'yunmall_excceed_code',
                'verbose_name': 'Excceed Code',
                'verbose_name_plural': 'Excced Codes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='fish',
            options={'verbose_name': 'Person', 'verbose_name_plural': 'Persons'},
        ),
    ]
