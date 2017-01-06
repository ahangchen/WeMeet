from django.db import models

from team.ctrl.defines import LONGTEXT_MAX_LENGTH, PATH_MAX_LENGTH, TEL_MAX_LENGTH, MAIL_MAX_LENGTH, NAME_MAX_LENGTH, \
    SHORT_TEXT_LENGTH, DATE_MAX_LENGTH, MEDIUM_TEXT_LENGTH, EXTRA_LONG_TEXT_LENGTH, SIMPLE_TEXT_LENGTH


class JobApply(models.Model):
    apply_id = models.AutoField(primary_key=True)
    # 学生。on_delete默认为CASCADE，当学生被删除的时候，投递关系级联删除
    stu = models.ForeignKey('StuInfo')
    # 职位，on_delete默认为CASCADE，当职位被删除的时候，投递关系级联删除
    job = models.ForeignKey('team.Job')
    # 投递状态，0表示待查看，1表示待沟通，2表示待面试，3表示录用， 4表示不合适
    state = models.IntegerField(default=0)
    # 状态更改时间
    change_time = models.CharField(max_length=DATE_MAX_LENGTH, blank=True, null=True, default='')
    # 团队，多app外键最好用字符串引用防止循环import，on_delete默认为CASCADE，当团队被删除的时候，投递关系级联删除
    team = models.ForeignKey('team.Team')
    # 简历文件路径
    resume_path = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=True, default='')
    # 投递时间
    apply_time = models.CharField(max_length=DATE_MAX_LENGTH, blank=True, null=True, default='')
    # 学生已阅读
    stu_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'job_apply'


class StuInfo(models.Model):
    id = models.AutoField(primary_key=True)
    # 姓名
    name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
    # 头衔
    title = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
    # 个性签名
    personal_signature = models.CharField(max_length=SHORT_TEXT_LENGTH, blank=True, null=True, default='')
    # 性别，0表示未填，1表示男，2表示女
    sex = models.IntegerField(default=0)
    # 学校
    school = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
    # 年级 枚举(值未定） -1 未选
    grade = models.IntegerField(default=0)
    # 头像路径
    avatar_path = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=True, default='')
    # 简历文件路径
    resume_path = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=True, default='')
    # 一级标签，0表示工程，1表示经管，2表示文艺，3表示人文 -1 未选
    label1 = models.IntegerField(default=0)
    # 人气数
    likes = models.IntegerField(default=0)

    class Meta:
        db_table = 'stu_info'


class StuLabel(models.Model):
    label2_id = models.AutoField(primary_key=True)
    # 二级标签
    text = models.CharField(max_length=SIMPLE_TEXT_LENGTH, blank=True, null=True, default='')
    # 学生，on_delete默认为CASCADE，当学生被删除的时候，账号级联删除
    stu = models.ForeignKey('StuInfo', null=False)

    class Meta:
        db_table = 'stu_label_2'


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

#
# class StuEdu(models.Model):
#     # By default, id = models.AutoField(primary_key=True)
#     # 专业
#     major = models.CharField(max_length=SHORT_TEXT_LENGTH, blank=True, null=True, default='')
#     # 毕业年份
#     graduation_year = models.IntegerField(default='-1')
#     # 学历 0表示其他，1表示大专，2表示本科，3表示硕士，4表示博士
#     background = models.IntegerField(default='-1')
#     # 学校
#     school = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
#     # 学生，on_delete默认为CASCADE，当学生被删除的时候，教育经历级联删除
#     stu = models.ForeignKey('StuInfo', null=False)
#
#     class Meta:
#         db_table = 'stu_edu'
#
#
# class StuIntern(models.Model):
#     intern_id = models.AutoField(primary_key=True)
#     # 公司
#     company = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
#     # 职位
#     position = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
#     # 开始年月
#     begin_time = models.CharField(max_length=DATE_MAX_LENGTH, blank=True, null=True, default='')
#     # 结束年月
#     end_time = models.CharField(max_length=DATE_MAX_LENGTH, blank=True, null=True, default='')
#     # 职能描述
#     description = models.CharField(max_length=LONGTEXT_MAX_LENGTH, blank=True, null=True, default='')
#     # 学生，on_delete默认为CASCADE，当学生被删除的时候，实习经历级联删除
#     stu = models.ForeignKey('StuInfo', null=False)
#
#     class Meta:
#         db_table = 'stu_intern'
#
#
# class StuProj(models.Model):
#     proj_id = models.AutoField(primary_key=True)
#     # 项目名称
#     name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
#     # 职位
#     duty = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
#     # 年份
#     year = models.CharField(max_length=DATE_MAX_LENGTH, blank=True, null=True, default='')
#     # 职能描述
#     description = models.CharField(max_length=LONGTEXT_MAX_LENGTH, blank=True, null=True, default='')
#     # 学生，on_delete默认为CASCADE，当学生被删除的时候，项目经历级联删除
#     stu = models.ForeignKey('StuInfo', null=False)
#
#     class Meta:
#         db_table = 'stu_proj'


class StuSkill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    # 技能名称
    name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True, null=True, default='')
    # 技能值0-10
    value = models.IntegerField(default=0)
    # 学生，on_delete默认为CASCADE，当学生被删除的时候，技能评价级联删除
    stu = models.ForeignKey('StuInfo', null=False)

    class Meta:
        db_table = 'stu_skill'


class StuAboutMe(models.Model):
    about_me_id = models.AutoField(primary_key=True)
    # 标题
    title = models.CharField(max_length=SHORT_TEXT_LENGTH, blank=False, null=True, default='')
    # 内容
    text = models.CharField(max_length=MEDIUM_TEXT_LENGTH, blank=False, null=True, default='')
    # 学生，on_delete默认为CASCADE，当学生被删除的时候，技能评价级联删除
    stu = models.ForeignKey('StuInfo', null=False)

    class Meta:
        db_table = 'stu_about_me'


class StuWorks(models.Model):
    works_id = models.AutoField(primary_key=True)
    # 作品名称
    name = models.CharField(max_length=NAME_MAX_LENGTH, blank=False, null=False, default='')
    # 职责
    duty = models.CharField(max_length=SHORT_TEXT_LENGTH, blank=False, null=False, default='')
    # 作品链接
    url = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=False, default='')
    # 描述
    description = models.CharField(max_length=EXTRA_LONG_TEXT_LENGTH, blank=True, null=False, default='')
    # 图片
    img = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=False, default='')
    # 音频
    audio = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=False, default='')
    # 视频
    video = models.CharField(max_length=PATH_MAX_LENGTH, blank=True, null=False, default='')
    # 学生，on_delete默认为CASCADE，当学生被删除的时候，技能评价级联删除
    stu = models.ForeignKey('StuInfo', null=False)

    class Meta:
        db_table = 'stu_works'


class StuItem(models.Model):
    # 自定义的模块
    title = models.CharField(max_length=SHORT_TEXT_LENGTH)
    content = models.CharField(max_length=LONGTEXT_MAX_LENGTH)
    stu = models.ForeignKey('StuInfo', null=False)
