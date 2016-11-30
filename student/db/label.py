"""
学生的二级标签
"""
from student.models import StuLabel

from student.util.logger import logger


def stu_filter(stu):
    """
    用学生查询二级标签
    返回QuerySet
    """
    return StuLabel.objects.filter(stu=stu)



