from django.db import models

from team.ctrl.defines import LONGTEXT_MAX_LENGTH, PATH_MAX_LENGTH, TEL_MAX_LENGTH, MAIL_MAX_LENGTH, NAME_MAX_LENGTH, \
    SHORT_TEXT_LENGTH, DATE_MAX_LENGTH


class JobApply(models.Model):
    # By default, id = models.AutoField(primary_key=True)
    stu = models.ForeignKey('StuInfo', models.DO_NOTHING)
    # 职位
    job = models.ForeignKey('team.Job')
    # 投递状态，0表示待查收，1表示面试中，2表示待发offer，3表示已结束
    state = models.IntegerField(default=0)
    # 学生简历
    resume = models.ForeignKey('Resume', models.DO_NOTHING)
    # 多app外键最好用字符串引用防止循环import
    team = models.ForeignKey('team.Team')
    # 简历类型，0表示网站模板简历，1表示附件简历
    resume_type = models.IntegerField(default=0)

    class Meta:
        db_table = 'job_apply'


class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    stu = models.ForeignKey('StuInfo', models.DO_NOTHING)
    resume_edu = models.CharField(max_length=LONGTEXT_MAX_LENGTH, blank=True, null=True)
    resume_internship = models.CharField(max_length=LONGTEXT_MAX_LENGTH, blank=True, null=True)
    resume_project = models.CharField(max_length=LONGTEXT_MAX_LENGTH, blank=True, null=True)
    resume_stu_work = models.CharField(max_length=LONGTEXT_MAX_LENGTH, blank=True, null=True)
    resume_award = models.CharField(max_length=LONGTEXT_MAX_LENGTH, blank=True, null=True)
    # 附件路径
    file_path = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=True)

    class Meta:
        db_table = 'resume'


class StuInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
    school = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
    tel = models.CharField(max_length=TEL_MAX_LENGTH, blank=True, null=True, default='')
    mail = models.CharField(max_length=MAIL_MAX_LENGTH, blank=True, null=True, default='')
    # 头像路径
    avatar_path = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=True, default='')
    # 学历
    edu_background = models.CharField(max_length=SHORT_TEXT_LENGTH, blank=True, null=True, default='')
    # 年级
    grade = models.CharField(max_length=SHORT_TEXT_LENGTH, blank=True, null=True, default='')
    # 专业
    major = models.CharField(max_length=SHORT_TEXT_LENGTH, blank=True, null=True, default='')
    # 所在地
    location = models.CharField(max_length=SHORT_TEXT_LENGTH, blank=True, null=True, default='')

    class Meta:
        db_table = 'stu_info'


class StuAccount(models.Model):
    # 账号（邮箱）
    account = models.CharField(primary_key=True, max_length=MAIL_MAX_LENGTH, null=False, blank=False)
    # 密码
    pwd = models.CharField(max_length=SHORT_TEXT_LENGTH, null=False, blank=False)
    # 激活状态
    is_activated = models.BooleanField(default=False)
    # 加密的账号
    ciphertext = models.CharField(max_length=LONGTEXT_MAX_LENGTH, null=True, blank=False)
    # 学生，on_delete默认为CASCADE，当学生被删除的时候，账号级联删除
    stu = models.ForeignKey('StuInfo', null=False)
    # 上一次重置账号的日期
    reset_date = models.CharField(max_length=DATE_MAX_LENGTH, null=False, blank=False)

    class Meta:
        db_table = 'stu_account'

