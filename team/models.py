from django.db import models

# Create your models here.
from team.ctrl.defines import LONGTEXT_MAX_LENGTH, PATH_MAX_LENGTH, TEL_MAX_LENGTH, MAIL_MAX_LENGTH, NAME_MAX_LENGTH, \
    SHORT_TEXT_LENGTH


# mysql 要求char字段需要有default
class Team(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, default='')
    logo_path = models.CharField(max_length=PATH_MAX_LENGTH, default='')
    # 团队联系方式
    contact_tel = models.CharField(max_length=TEL_MAX_LENGTH, default='')
    contact_mail = models.CharField(max_length=MAIL_MAX_LENGTH, default='')
    # 口号
    slogan = models.CharField(max_length=SHORT_TEXT_LENGTH, default='')
    # 团队介绍
    about = models.CharField(max_length=LONGTEXT_MAX_LENGTH, default='')
    # 发展历程
    history = models.CharField(max_length=LONGTEXT_MAX_LENGTH, default='')
    # 团队类型，枚举，用于分类搜索
    b_type = models.IntegerField(default=0)


class TeamStu(models.Model):
    # 防止没有primary key，所以不设置unique_together，用自动生成的id作为主键
    team = models.ForeignKey(Team)
    # http://stackoverflow.com/questions/5680414/django-import-error-from-foreign-key-in-another-application-model
    # 多app外键最好用字符串引用防止循环import
    stu = models.ForeignKey('student.StuInfo')


class TeamImg(models.Model):
    # 一个团队可能有多张图片啊摔
    team = models.ForeignKey(Team)
    path = models.CharField(max_length=PATH_MAX_LENGTH, default='')


class Label(models.Model):
    team = models.ForeignKey(Team)
    name = models.CharField(max_length=NAME_MAX_LENGTH, default='')


class Product(models.Model):
    team = models.ForeignKey(Team)
    content = models.CharField(max_length=LONGTEXT_MAX_LENGTH, default='')
    img_path = models.CharField(max_length=PATH_MAX_LENGTH, default='')
    reward = models.CharField(max_length=LONGTEXT_MAX_LENGTH, default='')
    # 上周访问量，每周日晚上置为week_visit_cnt
    last_visit_cnt = models.IntegerField(default=0)
    # 每周访问量，周日晚上清空
    week_visit_cnt = models.IntegerField(default=0)
    # 统计周热门项目时，用last_visit_cnt + week_visit_cnt作为筛选条件


class Job(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, default='')
    # start_time = models.DateTimeField(auto_now_add=True)
    # end_time = models.DateTimeField()
    # 职位类型：产品，开发，设计。。。
    j_type = models.IntegerField(default=0)
    # 工作类型：全职，兼职，实习
    w_type = models.IntegerField(default=0)
    min_salary = models.FloatField(default=0.0)
    max_salary = models.FloatField(default=0.0)
    # 工作地点，由省市区组成，每个概念为一个Int
    prince = models.IntegerField(default=0)
    city = models.IntegerField(default=0)
    town = models.IntegerField(default=0)
    address = models.CharField(max_length=SHORT_TEXT_LENGTH, default='')

    exp_cmd = models.CharField(max_length=SHORT_TEXT_LENGTH, default='')
    # 总结职位特点
    summary = models.CharField(max_length=SHORT_TEXT_LENGTH, default='')
    # 职位要求
    job_cmd = models.CharField(max_length=LONGTEXT_MAX_LENGTH, default='')
    # 任职要求
    work_cmd = models.CharField(max_length=LONGTEXT_MAX_LENGTH, default='')
    # 发布状态，0表示待发布，1表示已发布，2表示已下架
    pub_state = models.IntegerField(default=0)


class JobType(models.Model):
    # 职位类型：产品/设计/开发
    name = models.CharField(max_length=NAME_MAX_LENGTH, default='')


class WorkType(models.Model):
    # 工作类型：实习/兼职/全职
    name = models.CharField(max_length=NAME_MAX_LENGTH, default='')


class TeamType(models.Model):
    # 团队类型可以由管理员预设，在团队信息中设置类型id以区分团队类型
    name = models.CharField(max_length=NAME_MAX_LENGTH, default='')
