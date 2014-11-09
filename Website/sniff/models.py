# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Devices(models.Model):
    mac_address = models.CharField(db_column='MAC_address', primary_key=True, max_length=17)  # Field name made lowercase.
    type = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    owner = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'devices'


class FoundDevices(models.Model):
    found_id = models.IntegerField(primary_key=True)
    mac_address = models.CharField(db_column='MAC_address', max_length=17)  # Field name made lowercase.
    stations_id = models.IntegerField()
    time = models.CharField(max_length=255)

    class Meta:
        db_table = 'found_devices'


class Stations(models.Model):
    station_id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=255)
    notes = models.TextField()
    ip_address = models.CharField(max_length=16)
    mac_address = models.CharField(db_column='MAC_address', max_length=17)  # Field name made lowercase.

    class Meta:
        db_table = 'stations'
