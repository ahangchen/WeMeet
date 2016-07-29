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

from student.models import StuSkill
from student.util.logger import logger
from student.util import value_update
from student.util.value_update import NO_INPUT


def stu_filter(stu):
    """
    用学生查询技能评价
    返回QuerySet
    """
    return StuSkill.objects.filter(stu=stu)


def insert(name, value, stu):
    """
    插入技能评价
    成功：返回{'tag': OK_INSERT, 'skill': new_skill}
    失败：返回{'tag': ERR_INSERT_DB}
    """
    try:
        new_skill = StuSkill(name=name,
                             value=value,
                             stu=stu)

        new_skill.save()
        return {'tag': OK_INSERT,
                'skill': new_skill}
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致插入技能评价记录失败')
        return {'tag': ERR_INSERT_DB}


def id_stu_update(skill_id, stu, name=NO_INPUT, value=NO_INPUT):
    """
    用skill_id和stu更新技能评价
    成功：返回OK_UPDATE
    失败：返回ERR_UPDATE_DB
    @skill_id: 技能评价id
    @stu: 关联的学生
    @name: 技能名称
    @value: 评价值
    """
    try:
        update_skill = StuSkill.objects.all().get(skill_id=skill_id, stu=stu)

        update_skill.name = value_update.value(update_skill.name, name)
        update_skill.value = value_update.value(update_skill.value, value)

        update_skill.save()
        return OK_UPDATE

    except StuSkill.DoesNotExist:
        logger.warning("尝试更新学生id和技能评价id不匹配的技能评价")
        return ERR_UPDATE_DB
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致更新技能评价失败')
        return ERR_UPDATE_DB


def id_stu_delete(skill_id, stu):
    """
    用skill_id和stu删除技能评价
    成功：返回OK_DELETE
    失败：返回ERR_DELETE_DB
    """
    try:
        delete_skill = StuSkill.objects.all().get(skill_id=skill_id, stu=stu)  # 抛出MultipleObjectsReturned或DoesNotExist
        delete_skill.delete()  # 不抛出异常
        return OK_DELETE

    except StuSkill.DoesNotExist:
        logger.error('尝试删除学生id和技能评价id不匹配的技能评价')
        return ERR_DELETE_DB

    except StuSkill.MultipleObjectsReturned:
        logger.info('数据库异常（存在重复记录）')
        StuSkill.objects.all().filter(skill_id=skill_id, stu=stu).delete()  # 不抛异常
        return OK_DELETE

    # 数据库异常
    except Exception as e:
        logger.error(e.__str__() + '数据库异常导致删除项目技能评价失败')
        return ERR_DELETE_DB
