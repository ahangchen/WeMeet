from django.db import models

# Create your models here.
from student.models import StuInfo


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    about = models.CharField(max_length=600)
    logo_path = models.CharField(max_length=200)
    strength = models.CharField(max_length=600)
    contact_tel = models.CharField(max_length=20)
    contact_mail = models.CharField(max_length=40)


class TeamStu(models.Model):
    team = models.ForeignKey(Team)
    stu = models.ForeignKey(StuInfo)


class Product(models.Model):
    team = models.ForeignKey(Team)
    content = models.CharField(max_length=600)


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    content = models.CharField(max_length=600)

