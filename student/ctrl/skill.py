from student.ctrl.tag import OK_GET_SKILL, ERR_GET_NO_SKILL, ERR_GET_SKILL_DB, \
                             OK_ADD_SKILL, ERR_ADD_SKILL_DB, \
                             OK_UPDATE_SKILL, ERR_UPDATE_SKILL_DB, \
                             OK_DEL_SKILL, ERR_DEL_SKILL_DB

from student.db import stu_info, skill
from student.util.logger import logger


def get(stu_id):
    """
    获取技能评价
    成功：{'tag': OK_GET_SKILL, 'skill_list': list(filter_set.values())}
                            "skill_list": [{
            　　　　　　                      "skill_id": skill_id,
            　　　　　　                      "name": name,
            　　　　　　                      "value": value},
            　　　                         ...]}
    失败：{'tag': ERR_GET_NO_SKILL}或{'tag': ERR_GET_SKILL_DB}
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        filter_set = skill.stu_filter(stu=select_rlt['stu'])

        # 如果该学生有合法的技能评价数量
        if filter_set.count() != 0:
            return {'tag': OK_GET_SKILL,
                    'skill_list': list(filter_set.values())}

        # 如果该学生无技能评价 filter_set.count() == 0
        else:
            return {'tag': ERR_GET_NO_SKILL}

    # 如果学生不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试获取不存在的学生的技能评价')
        return {'tag': ERR_GET_SKILL_DB}
    # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，查询技能评价失败')
        return {'tag': ERR_GET_SKILL_DB}


def add(stu_id, name, value):
    """
    增加技能评价
    成功：返回{'tag': OK_ADD_SKILL, 'skill_id': insert_rlt['skill'].skill_id}
    失败：返回{'tag': ERR_ADD_SKILL_DB}
    @stu_id:关联的学生id
    @name: 技能名称
    @duty: 技能值
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        insert_rlt = \
            skill.insert(name=name, value=value, stu=select_rlt['stu'])
        # 如果插入成功：
        if insert_rlt['tag'] == skill.OK_INSERT:
            return {'tag': OK_ADD_SKILL,
                    'skill_id': insert_rlt['skill'].skill_id}
        # 如果插入失败（insert_rlt['tag'] == ERR_INSERT_DB）
        else:
            return {'tag': ERR_ADD_SKILL_DB}

    # 如果学生记录不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试为不存在的学生增加技能评价')
        return {'tag': ERR_ADD_SKILL_DB}
    # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，增加技能评价失败')
        return {'tag': ERR_ADD_SKILL_DB}


def update(skill_id, stu_id, name, value):
    """
    修改技能评价
    成功：返回{'tag': OK_UPDATE_SKILL}
    失败：返回{'tag': ERR_UPDATE_SKILL_DB}
    @skill_id: 技能评价的id
    @stu_id:  关联的学生id
    @name: 技能名称
    @value: 技能值
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        update_tag = \
            skill.id_stu_update(skill_id, select_rlt['stu'], name, value)

        # 如果更新成功
        if update_tag == skill.OK_UPDATE:
            return {'tag': OK_UPDATE_SKILL}
        # 如果更新失败
        else:
            return {'tag': ERR_UPDATE_SKILL_DB}

    # 如果学生不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试更新不存在的学生的技能评价')
        return {'tag': ERR_UPDATE_SKILL_DB}
    # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，修改技能评价失败')
        return {'tag': ERR_UPDATE_SKILL_DB}


def delete(stu_id, skill_id):
    """
    删除技能评价
    成功：返回{'tag': OK_DEL_SKILL}
    失败：返回{'tag': ERR_DEL_SKILL_DB}
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == stu_info.OK_SELECT:
        delete_tag = skill.id_stu_delete(skill_id, select_rlt['stu'])
        if delete_tag == skill.OK_DELETE:
            return {'tag': OK_DEL_SKILL}

        # delete_tag == ERR_DELETE_DB
        else:
            return {'tag': ERR_DEL_SKILL_DB}

    # 如果学生不存在
    elif select_rlt['tag'] == stu_info.ERR_SELECT_NOTEXIST:
        logger.warning('尝试删除不存在的学生的技能评价')
        return {'tag': ERR_DEL_SKILL_DB}

    # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致无法确认学生是否存在，删除技能评价失败')
        return {'tag': ERR_DEL_SKILL_DB}
