# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class StuInfo(models.Model):
    stu_id = models.AutoField(primary_key=True)
    stu_name = models.CharField(max_length=44)
    stu_tel = models.CharField(max_length=20, blank=True, null=True)
    stu_mail = models.CharField(max_length=45)
    stu_want = models.CharField(max_length=400, blank=True, null=True)
    resume_path = models.CharField(max_length=200, blank=True, null=True)
    my_meet = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stu_info'
