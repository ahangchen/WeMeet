# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class JobApply(models.Model):
    # By default, id = models.AutoField(primary_key=True)
    stu = models.ForeignKey('StuInfo', models.DO_NOTHING)
    job_id = models.CharField(max_length=45)
    stu_job_state = models.CharField(max_length=45)
    resume = models.ForeignKey('Resume', models.DO_NOTHING)
    team_id = models.CharField(max_length=45)
    resume_type = models.IntegerField()

    class Meta:
        db_table = 'job_apply'


class Resume(models.Model):
    resume_id = models.AutoField(primary_key=True)
    stu = models.ForeignKey('StuInfo', models.DO_NOTHING)
    resume_edu = models.CharField(max_length=600, blank=True, null=True)
    resume_internship = models.CharField(max_length=1000, blank=True, null=True)
    resume_project = models.CharField(max_length=1000, blank=True, null=True)
    resume_stu_work = models.CharField(max_length=600, blank=True, null=True)
    resume_award = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        db_table = 'resume'


class StuInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=45)
    pwd = models.CharField(max_length=32)
    name = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=45, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    mail = models.CharField(max_length=45, blank=True, null=True)
    avatar_path = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'stu_info'
