from student.db.tag import ERR_DELETE_DB
from student.db.tag import ERR_UPDATE_NOTEXIST
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import ERR_INSERT_DB
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_SELECT_DB
from student.db.tag import OK_DELETE
from student.db.tag import OK_INSERT
from student.db.tag import OK_UPDATE
from student.db.tag import OK_SELECT

from student.models import StuProj
from student.util.logger import logger
from student.util.value_update import value, NO_INPUT


def stu_filter(stu):
    """
    用学生查询项目记录
    返回QuerySet
    """
    return StuProj.objects.filter(stu=stu)


def insert(name, duty, year, description, stu):
    """
    插入项目经历
    成功：返回{'tag': OK_INSERT, 'new_proj': new_proj}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_proj = StuProj(name=name,
                           duty=duty,
                           year=year,
                           description=description,
                           stu=stu)

        new_proj.save()
        return {'tag': OK_INSERT,
                'proj': new_proj}
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致插入项目经历记录失败')
        return {'tag': ERR_INSERT_DB}


def id_stu_update(proj_id, stu, name=NO_INPUT, duty=NO_INPUT, year=NO_INPUT, description=NO_INPUT):
    """
    用proj_id和stu更新项目经历
    成功：返回OK_UPDATE
    失败：返回ERR_UPDATE_DB
    @proj_id: 项目id
    @stu: 关联的学生
    @name: 项目名称
    @duty: 职责
    @year: 年份
    @description: 描述
    """
    try:
        update_proj = StuProj.objects.all().get(proj_id= proj_id, stu=stu)

        update_proj.name = value(update_proj.name, name)
        update_proj.duty = value(update_proj.duty, duty)
        update_proj.year = value(update_proj.year, year)
        update_proj.description = value(update_proj.description, description)

        update_proj.save()
        return OK_UPDATE

    except StuProj.DoesNotExist:
        logger.warning("尝试更新学生id和项目经历id不匹配的项目经历")
        return ERR_UPDATE_DB
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致更新项目经历失败')
        return ERR_UPDATE_DB


def id_stu_delete(proj_id, stu):
    """
    用id和stu删除项目经历
    成功：返回OK_DELETE
    失败：返回ERR_DELETE_DB
    """
    try:
        delete_proj = StuProj.objects.all().get(proj_id=proj_id, stu=stu)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_proj.delete()  # 不抛出异常
        return OK_DELETE

    except StuProj.DoesNotExist:
        logger.error('尝试删除学生id和项目经历id不匹配的项目经历')
        return ERR_DELETE_DB

    except StuProj.MultipleObjectsReturned:
        logger.info('数据库异常（存在重复记录）')
        StuProj.objects.all().filter(proj_id=proj_id, stu=stu).delete()  # 不抛异常
        return OK_DELETE

    # 数据库异常
    except Exception as e:
        logger.error(e.__str__()+ '数据库异常导致删除项目经历失败')
        return ERR_DELETE_DB
