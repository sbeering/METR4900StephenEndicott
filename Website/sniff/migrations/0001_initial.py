# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('mac_address', models.CharField(max_length=17, serialize=False, primary_key=True, db_column='MAC_address')),
                ('type', models.CharField(max_length=255, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('owner', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'db_table': 'devices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoundDevices',
            fields=[
                ('found_id', models.IntegerField(serialize=False, primary_key=True)),
                ('mac_address', models.CharField(max_length=17, db_column='MAC_address')),
                ('stations_id', models.IntegerField()),
                ('time', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'found_devices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stations',
            fields=[
                ('station_id', models.IntegerField(serialize=False, primary_key=True)),
                ('location', models.CharField(max_length=255)),
                ('notes', models.TextField()),
                ('ip_address', models.CharField(max_length=16)),
                ('mac_address', models.CharField(max_length=17, db_column='MAC_address')),
            ],
            options={
                'db_table': 'stations',
            },
            bases=(models.Model,),
        ),
    ]
