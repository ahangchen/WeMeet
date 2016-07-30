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

from student.models import StuIntern
from student.util.logger import logger
from student.util.value_update import value, NO_INPUT

def stu_filter(stu):
    """
    用学生查询实习经历记录
    返回QuerySet
    """
    return StuIntern.objects.filter(stu=stu)


def insert(company, position, begin_time, end_time, description, stu):
    """
    插入实习经历
    成功：返回{'tag': OK_INSERT, 'intern': new_intern}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_intern = StuIntern(company=company,
                               position=position,
                               begin_time=begin_time,
                               end_time=end_time,
                               description=description,
                               stu=stu)

        new_intern.save()
        return {'tag': OK_INSERT,
                'intern': new_intern}
    except Exception as e:
        logger.error(e.__str__()+ '数据库异常导致插入实习经历记录失败')
        return {'tag': ERR_INSERT_DB}


def id_stu_update(intern_id, stu, company=NO_INPUT, position=NO_INPUT, begin_time=NO_INPUT,
                  end_time=NO_INPUT, description=NO_INPUT):
    """
    用intern_id和stu更新实习经历
    @company: 公司
    @position: 职位
    @begin_time: 开始时间
    @end_time: 结束时间
    @description: 描述
    @stu: 关联的学生
    成功：返回
    失败：返回
    """
    try:
        update_intern = StuIntern.objects.all().get(intern_id= intern_id, stu=stu)

        update_intern.company = value(update_intern.company, company)
        update_intern.position = value(update_intern.position, position)
        update_intern.begin_time = value(update_intern.begin_time, begin_time)
        update_intern.end_time = value(update_intern.end_time, end_time)
        update_intern.description = value(update_intern.description, description)

        update_intern.save()
        return OK_UPDATE

    except StuIntern.DoesNotExist:
        logger.warning("尝试更新学生id和实习经历id不匹配的实习经历")
        return ERR_UPDATE_DB
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致更新实习经历失败')
        return ERR_UPDATE_DB


def id_stu_delete(intern_id, stu):
    """
    用id和stu删除实习经历
    成功：返回OK_DELETE
    失败：返回ERR_DELETE_DB
    """
    try:
        delete_intern = StuIntern.objects.all().get(intern_id=intern_id, stu=stu)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_intern.delete()  # 不抛出异常
        return OK_DELETE

    except StuIntern.DoesNotExist:
        logger.error('尝试删除学生id和实习经历id不匹配的实习经历')
        return ERR_DELETE_DB

    except StuIntern.MultipleObjectsReturned:
        logger.info('数据库异常（存在重复记录）')
        StuIntern.objects.all().filter(intern_id=intern_id, stu=stu).delete()  # 不抛异常
        return OK_DELETE

    # 数据库异常
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致删除实习经历失败')
        return ERR_DELETE_DB
