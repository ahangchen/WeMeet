
from student.models import StuProj


def stu_filter(stu):
    """
    用学生查询项目记录
    返回QuerySet
    """
    return StuProj.objects.filter(stu=stu)
