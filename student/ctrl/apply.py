from student.db.tag import OK_SELECT, ERR_SELECT_NOTEXIST, ERR_SELECT_DB

from student.ctrl.tag import OK_GET_APPLY, ERR_GET_NO_APPLY, ERR_GET_APPLY_DB

from student.db import stu_info, job_apply
from team.db import job, team
from student.util.logger import logger


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


def stu_get_apply(stu_id, state):
    """
    学生获取投递信息
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