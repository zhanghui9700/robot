# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yunmall', '0002_add_code_mobile_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPBlack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('delete_date', models.DateTimeField(null=True, blank=True)),
                ('fish', models.ForeignKey(related_name='sources', db_constraint=False, to='yunmall.Fish', null=True)),
            ],
            options={
                'db_table': 'yunmall_ip_black',
                'verbose_name': 'Black IP',
                'verbose_name_plural': 'Black IP',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IPPool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('delete_date', models.DateTimeField(null=True, blank=True)),
                ('ip_int', models.BigIntegerField(default=0, unique=True, verbose_name='IP')),
                ('ip_str', models.CharField(unique=True, max_length=64)),
                ('count', models.IntegerField(default=1, verbose_name='IP Count')),
            ],
            options={
                'db_table': 'yunmall_ip_pool',
                'verbose_name': 'IP',
                'verbose_name_plural': 'IPs',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ipblack',
            name='ip',
            field=models.ForeignKey(related_name='blacks', db_constraint=False, to='yunmall.IPPool', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='config',
            name='conf',
            field=models.CharField(unique=True, max_length=128, verbose_name='Config', choices=[(b'paused', '\u6682\u505c\u6267\u884c'), (b'day_quota', '\u6bcf\u65e5\u6ce8\u518c\u9650\u989d')]),
            preserve_default=True,
        ),
    ]
