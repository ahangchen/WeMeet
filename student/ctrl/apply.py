from student.db.tag import OK_SELECT, ERR_SELECT_NOTEXIST, ERR_SELECT_DB, \
                           OK_UPDATE, ERR_UPDATE_DB

from student.ctrl.tag import OK_GET_APPLY, ERR_GET_NO_APPLY, ERR_GET_APPLY_DB, \
                             OK_HANDLE, ERR_HANDLE_DB, ERR_STATE, \
                             OK_READ_APPLY, ERR_READ_APPLY_DB, \
                             OK_APPLY_INFO, ERR_APPLY_INFO_DB, \
                             OK_REPLY, ERR_REPLY_DB, \
                             OK_DUMP, ERR_DUMP_DB

from student.db import stu_info, job_apply
from team.db import job, team
from student.util.logger import logger
from student.util.date_helper import curr_year, curr_month

from django.core.mail import send_mail


def dump_stu_apply(stu, state, rlt_list):
    """
    从JobApply的QuerySet里获取学生查询投递关系所需要的信息
    """
    apply_set = job_apply.stu_state_filter(stu=stu, state=state)
    for apply in apply_set:
        apply_job = job.id_job(apply.job_id)
        apply_team = team.id_team(apply_job.team_id)
        contact_mail = team.team_mail(apply_job.team_id)
        rlt_list.append({'apply_id': apply.apply_id,
                         'state': state,
                         'job_id': apply.job_id,
                         'is_read': apply.stu_read,
                         'job_name': apply_job.name,
                         'prince': apply_job.prince,
                         'city': apply_job.city,
                         'town': apply_job.town,
                         'address': apply_job.address,
                         'team_name': apply_team.name,
                         'min_salary': apply_job.min_salary,
                         'max_salary': apply_job.max_salary,
                         'change_time': apply.change_time,
                         'contact': apply_team.leader,
                         'mail': contact_mail
                         })


def dump_team_apply(team, state, rlt_list, unread_num):
    """
    从JobApply的QuerySet里获取团队查询投递关系所需要的信息
    """
    apply_set = job_apply.team_state_filter(team=team, state=state)
    for apply in apply_set:
        apply_job = job.id_job(apply.job_id)
        select_rlt = stu_info.select(apply.stu_id)

        # 如果数据库异常导致无法查询投递关联的学生
        if select_rlt['tag'] != OK_SELECT:
            logger.error('数据库异常导致无法查询apply_id为%s的投递关联的学生' % (apply.apply_id))
            return ERR_DUMP_DB

        is_read = True
        if state == 0:
            is_read = False

        # 如果获取学生成功
        apply_stu = select_rlt['stu']
        rlt_list.append({'apply_id': apply.apply_id,
                         'state': state,
                         'job_id': apply.job_id,
                         'stu_id': apply.stu_id,
                         'job_name': apply_job.name,
                         'stu_name': apply_stu.name,
                         'apply_time': apply.apply_time,
                         'is_read': int(is_read)
                         })

        if not is_read:
            unread_num[0] += 1

    return OK_DUMP


def stu_get_list(stu_id, state):
    """
    学生获取投递列表
    @stu_id: 学生id
    @state: 投递状态，0表示待查看，1表示待沟通，2表示待面试，3表示录用， 4表示不合适，5表示全部
    成功：返回{
                'tag': OK_GET_APPLY,
                'apply_list': apply_list
            }
    失败：返回{'tag': ERR_GET_NO_APPLY}或{'tag': ERR_GET_APPLY_DB}
    """
    state = int(state)
    select_rlt = stu_info.select(stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        apply_list = []
        if state == 5:
            for s in range(1, 5):
                dump_stu_apply(stu=select_rlt['stu'], state=s, rlt_list=apply_list)

            if not apply_list:
                return {'tag': ERR_GET_NO_APPLY}
            return {
                'tag': OK_GET_APPLY,
                'apply_list': apply_list
            }

        elif state in range(1, 5):
            dump_stu_apply(stu=select_rlt['stu'], state=state, rlt_list=apply_list)

            if not apply_list:
                return {'tag': ERR_GET_NO_APPLY}

            return {
                'tag': OK_GET_APPLY,
                'apply_list': apply_list
            }

        else:
            logger.warning('尝试用不合法的状态查询投递记录')
            return {'tag': ERR_GET_APPLY_DB}


        # 如果学生不存在
    elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试获取不存在学生的投递信息')
        return {'tag': ERR_GET_APPLY_DB}
    # 如果数据库异常导致无法确认学生是否存在
    else:
        logger.error('数据库异常导致无法确认学生是否存在,获取学生的投递信息失败')
        return {'tag': ERR_GET_APPLY_DB}


def set_read(apply_list):
    """
    设置投递记录为已读(学生)
    成功：返回{'tag': OK_READ_APPLY}
    失败：返回{'tag': ERR_READ_APPLY_DB}
    """
    fail_tag = False
    for apply_id in apply_list:
        update_tag = job_apply.update(apply_id=apply_id, stu_read=True)
        # 如果更新失败(update_tag == ERR_UPDATE_DB)
        if update_tag == ERR_UPDATE_DB:
            logger.warning('apply_id为%s的投递记录设置已读失败' % apply_id)
            fail_tag = True

    # 如果更新成功
    if not fail_tag:
        return {'tag': OK_READ_APPLY}
    # 如果更新失败(fail_tag)
    else:
        return {'tag': ERR_READ_APPLY_DB}


def team_get_list(team_id, state):

    """
    团队获取投递列表
    @team_id: 团队id
    @state: 投递状态，0表示新接收，1表示待沟通，2表示待面试，3表示完成
    成功：返回{
                    'tag': OK_GET_APPLY,
                    'unread_num': unread_num,
                    'apply_list': apply_list
                }
    失败：返回{'tag': ERR_GET_NO_APPLY}或{'tag': ERR_GET_APPLY_DB}
    """
    state = int(state)
    select_team = team.id_team(team_id)
    if select_team is not None:
        apply_list = []
        unread_num = [0]
        # （输入值）3表示完成，包括录用(返回值3)和不合适（返回值4）
        if state == 3:
            fail_tag = False
            for state in range(3, 5):
                dump_tag = dump_team_apply(select_team, state, apply_list, unread_num)
                if dump_tag == ERR_DUMP_DB:
                    fail_tag = True

            # 如果获取所需信息成功
            if not fail_tag:
                # 如果投递列表为空
                if not apply_list:
                    return {'tag': ERR_GET_NO_APPLY}
                # 如果投递列表不为空
                return {
                    'tag': OK_GET_APPLY,
                    'unread_num': unread_num[0],
                    'apply_list': apply_list
                }
            # 如果数据库异常导致获取所需的信息失败
            else:
                return {'tag': ERR_GET_APPLY_DB}

        elif state in range(0, 3):
            dump_tag = dump_team_apply(select_team, state, apply_list, unread_num)
            # 如果获取所需信息成功
            if dump_tag == OK_DUMP:

                # 如果投递列表为空
                if not apply_list:
                    return {'tag': ERR_GET_NO_APPLY}
                # 如果投递列表不为空
                return {
                    'tag': OK_GET_APPLY,
                    'unread_num': unread_num[0],
                    'apply_list': apply_list
                }

            # 如果数据库异常导致获取所需的信息失败
            else:
                return {'tag': ERR_GET_APPLY_DB}

        # 如果state不合法
        else:
            logger.warning('尝试用不合法的状态查询投递记录')
            return {'tag': ERR_GET_APPLY_DB}

    # 如果团队不存在
    else:
        logger.warning('尝试获取不存在团队的投递信息')
        return {'tag': ERR_GET_APPLY_DB}


def team_get_info(apply_id):
    """
    团队获取投递信息
    成功：返回{'tag': OK_APPLY_INFO,
                    'stu_id': apply.stu_id,
                    'name': stu.name,
                    'avatar_path': stu.avatar_path,
                    'sex': stu.sex,
                    'age': stu.age,
                    'mail': stu.mail,
                    'tel': stu.tel,
                    'school': stu.school,
                    'major': stu.major,
                    'location': stu.location,
                    'resume_path': apply.resume_path,
                    'state': apply.state
                    }
    失败：返回{'tag': ERR_APPLY_INFO_DB}
    """
    apply_select_rlt = job_apply.id_select(apply_id)

    # 如果查询投递记录成功
    if apply_select_rlt['tag'] == OK_SELECT:
        apply = apply_select_rlt['apply']
        stu_select_rlt = stu_info.select(apply.stu_id)

        # 如果获取关联的学生成功
        if stu_select_rlt['tag'] == OK_SELECT:
            stu = stu_select_rlt['stu']
            age = curr_year() - stu.year
            if curr_month() < stu.month:
                age -= 1
            return {'tag': OK_APPLY_INFO,
                    'stu_id': apply.stu_id,
                    'name': stu.name,
                    'avatar_path': stu.avatar_path,
                    'sex': stu.sex,
                    'age': age,
                    'mail': stu.mail,
                    'tel': stu.tel,
                    'school': stu.school,
                    'major': stu.major,
                    'location': stu.location,
                    'resume_path': apply.resume_path,
                    'state': apply.state
                    }

        # 如果无法获取关联的学生
        else:
            logger.error('数据库异常，无法获取与投递记录关联的学生信息')
            return {'tag': ERR_APPLY_INFO_DB}

    # 如果投递记录不存在
    elif apply_select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试获取不存在的投递记录的信息')
        return {'tag': ERR_APPLY_INFO_DB}
    # 如果数据库异常导致获取投递信息失败
    else:
        return {'tag': ERR_APPLY_INFO_DB}


def reply(apply_id, text):
    """
    邮件回复投递（团队）
    @apply_id:
    @text: 邮件内容
    成功：返回OK_REPLY
    失败：返回ERR_REPLY_DB
    """
    apply_select_rlt = job_apply.id_select(apply_id)

    # 如果查询投递记录成功
    if apply_select_rlt['tag'] == OK_SELECT:
        apply = apply_select_rlt['apply']
        stu_select_rlt = stu_info.select(apply.stu_id)

        # 如果获取关联的学生成功
        if stu_select_rlt['tag'] == OK_SELECT:
            mail = stu_select_rlt['stu'].mail
            send_mail('WeMeet投递职位回复邮件', text, 'm18826076291@sina.com', [mail])  # TODO(hjf): 修改邮件标题、发送邮箱
            return OK_REPLY

        # 如果无法获取关联的学生
        else:
            logger.error('数据库异常，无法获取与投递记录关联的学生信息')
            return ERR_REPLY_DB

    # 如果投递记录不存在
    elif apply_select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试回复不存在的投递')
        return ERR_REPLY_DB
    # 如果数据库异常导致获取投递信息失败
    else:
        return ERR_REPLY_DB


def handle(apply_id, new_state):
    """
    处理投递（团队）
    @apply_id:
    @state: 投递状态，1表示待沟通，2表示待面试，3表示录用， 4表示不合适
    成功：返回OK_HANDLE
    失败：返回ERR_STATE或ERR_HANDLE_DB
    """
    new_state = int(new_state)

    if new_state not in range(1, 5):
        logger.warning('尝试用不合法的state处理投递')
        return ERR_STATE

    apply_select_rlt = job_apply.id_select(apply_id)
    # 如果查询投递记录成功
    if apply_select_rlt['tag'] == OK_SELECT:
        update_tag = job_apply.update(apply_id=apply_id, state=new_state, stu_read=False)

        # 如果处理成功
        if update_tag == OK_UPDATE:
            return OK_HANDLE
        # 如果处理失败(update_tag == ERR_UPDATE_DB)
        else:
            return ERR_HANDLE_DB

    # 如果投递记录不存在
    elif apply_select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.warning('尝试处理不存在的投递记录的信息')
        return ERR_HANDLE_DB
    # 如果数据库异常导致获取投递信息失败
    else:
        return ERR_HANDLE_DB
