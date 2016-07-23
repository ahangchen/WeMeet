
from student.models import StuSkill


def stu_filter(stu):
    """
    用学生查询技能评价
    返回QuerySet
    """
    return StuSkill.objects.filter(stu=stu)
