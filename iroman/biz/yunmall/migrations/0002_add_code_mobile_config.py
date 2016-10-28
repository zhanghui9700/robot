# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yunmall', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('delete_date', models.DateTimeField(null=True, blank=True)),
                ('conf', models.CharField(unique=True, max_length=128, verbose_name='Config')),
                ('value', models.CharField(max_length=128, verbose_name='Value')),
                ('description', models.CharField(max_length=128, verbose_name='Description')),
            ],
            options={
                'db_table': 'yunmall_config',
                'verbose_name': 'Config',
                'verbose_name_plural': 'Config',
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='ExcceedMobile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('delete_date', models.DateTimeField(null=True, blank=True)),
                ('mobile', models.CharField(unique=True, max_length=32)),
            ],
            options={
                'db_table': 'yunmall_excceed_mobile',
                'verbose_name': 'Excceed Mobile',
                'verbose_name_plural': 'Excced Mobile',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='fish',
            options={'verbose_name': 'Person', 'verbose_name_plural': 'Persons'},
        ),
        migrations.AlterField(
            model_name='fish',
            name='code',
            field=models.CharField(max_length=128, unique=True, null=True, verbose_name='Invate Code'),
            preserve_default=True,
        ),
    ]
