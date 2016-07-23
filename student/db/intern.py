
from student.models import StuIntern


def stu_filter(stu):
    """
    用学生查询实习经历记录
    返回QuerySet
    """
    return StuIntern.objects.filter(stu=stu)
