from django.db import models

# Create your models here.


class Team(models.Model):
    about = models.CharField(max_length=600)
    logo_path = models.CharField(max_length=200)
    strength = models.CharField(max_length=600)
    contact_tel = models.CharField(max_length=20)
    contact_mail = models.CharField(max_length=40)


class TeamStu(models.Model):
    # 防止没有primary key，所以不设置unique_together，用自动生成的id作为主键
    team = models.ForeignKey(Team)
    # http://stackoverflow.com/questions/5680414/django-import-error-from-foreign-key-in-another-application-model
    # 多app外键最好用字符串引用防止循环import
    stu = models.ForeignKey('student.StuInfo')


class Product(models.Model):
    team = models.ForeignKey(Team)
    content = models.CharField(max_length=600)


class Job(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    content = models.CharField(max_length=600)

