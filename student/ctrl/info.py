from student.ctrl.tag import ERR_GET_INFO_DB
from student.ctrl.tag import ERR_GET_INFO_NOTEXIST
from student.ctrl.tag import ERR_UPDATE_STU_INFO_DB
from student.ctrl.tag import OK_GET_INFO
from student.ctrl.tag import OK_UPDATE_STU_INFO
from student.db.tag import ERR_SELECT_NOTEXIST
from student.db.tag import ERR_UPDATE_DB
from student.db.tag import ERR_UPDATE_NOTEXIST
from student.db.tag import OK_SELECT
from student.db.tag import OK_UPDATE
from student.util.logger import logger


WORKS_PATH_ROOT = 'student/works'


def get(stu_id):
    """
    获取学生信息
     成功：返回{'tag': OK_GET_INFO, 'stu': select_rlt['stu']}
     失败:返回{'tag': ERR_GET_INFO_NOTEXIST}
           或{'tag': ERR_GET_INFO_DB}
    """
    select_rlt = stu_info.select(stu_id=stu_id)
    # 如果学生存在
    if select_rlt['tag'] == OK_SELECT:
        return {'tag': OK_GET_INFO,
                'stu': select_rlt['stu']}
    # 如果学生记录不存在
    elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
        logger.error('学生不存在，获取学生信息失败')
        return {'tag': ERR_GET_INFO_NOTEXIST}
    # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
    else:
        logger.error('数据库异常导致获取学生信息失败')
        return {'tag': ERR_GET_INFO_DB}


def update(stu_id, name, title, personal_signature, sex, school, grade, avatar_path, label):
    """
    更新学生信息
    成功：返回OK_UPDATE_INFO
    失败：返回ERR_UPDATE_DB
    """

    stu_update_tag = stu_info.update(stu_id=stu_id,
                                     name=name,
                                     title=title,
                                     personal_signature=personal_signature,
                                     sex=int(sex),
                                     school=school,
                                     grade=int(grade),
                                     avatar_path=avatar_path,
                                     label=int(label))

    # 如果学生信息更新成功
    if stu_update_tag == OK_UPDATE:
        return OK_UPDATE_STU_INFO
    elif stu_update_tag == ERR_UPDATE_NOTEXIST:
        logger.error('学生不存在，无法更新学生信息')
        return ERR_UPDATE_STU_INFO_DB
    # 如果stu_update_tag == ERR_UPDATE_DB
    else:
        logger.error('数据库异常导致更新学生信息失败')
        return ERR_UPDATE_DB


# def add_edu(stu_id, major, graduation_year, background, school):
#     """
#     增加教育经历
#     成功：返回{'tag': OK_ADD_EDU, 'edu_id': insert_rlt['edu'].id}
#     失败：返回{'tag': ERR_ADD_EDU_FULL}
#            或{'tag': ERR_ADD_EDU_DB}
#     @stu_id: 学生id
#     @major: 专业
#     @graduation_year: 毕业年份
#     @background: 学历
#     @school: 学校
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         # 如果教育经历未达五条
#         if edu.stu_filter(stu=select_rlt['stu']).count() < 5:
#             insert_rlt = edu.insert(major=major, graduation_year=graduation_year,
#                                     background=background, school=school, stu=select_rlt['stu'])
#             # 如果插入成功：
#             if insert_rlt['tag'] == OK_INSERT:
#                 edu_id = insert_rlt['edu'].id
#                 get_rlt = get_edu(stu_id)
#                 # 如果获取教育经历列表成功
#                 if get_rlt['tag'] == OK_GET_EDU:
#                     return {'tag': OK_ADD_EDU,
#                             'edu_id': edu_id,
#                             'grade': get_rlt['grade'],
#                             'edu_background': get_rlt['edu_background']}
#
#                 # 如果获取教育经历列表失败
#                 else:
#                     logger.error('数据库异常无法获取学生信息中的grade和edu_background，导致增加教育经历失败')
#                     # 回滚
#                     edu.delete(edu_id)
#                     return {'tag': ERR_ADD_EDU_DB}
#
#             # 如果插入失败（insert_rlt['tag'] == ERR_INSERT_DB）
#             else:
#                 return {'tag': ERR_ADD_EDU_DB}
#
#         # 如果教育经历已有五条或更多
#         else:
#             return {'tag': ERR_ADD_EDU_FULL}
#
#     # 如果学生记录不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试为不存在的学生增加教育经历')
#         return {'tag': ERR_ADD_EDU_DB}
#     # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，增加教育经历失败')
#         return {'tag': ERR_ADD_EDU_DB}
#
#
# def get_edu(stu_id):
#     """
#     获取学生的教育经历
#     成功：返回{'tag': OK_GET_EDU, 'grade': latest_year, 'major': major, 'edu_list': edu_list}
#                      edu_list: [{'edu_id': edu_rcd.id,
#                                  'major': edu_rcd.major,
#                                  'graduation_year': edu_rcd.graduation_year,
#                                  'edu_background': edu_rcd.background,
#                                  'school': edu_rcd.school}]
#     失败：返回{'tag': ERR_GET_NO_EDU}
#           或{'tag': ERR_GET_EDU_DB}
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         filter_set = edu.stu_filter(stu=select_rlt['stu'])
#
#         # 如果该学生有合法的教育经历数量
#         if filter_set.count() in range(1, 6):
#             edu_list = []
#             latest_year = -1
#             edu_background = -1
#             for edu_rcd in filter_set:
#                 if edu_rcd.background >= edu_background:
#                     latest_year = edu_rcd.graduation_year
#                     edu_background = edu_rcd.background
#                 edu_list.append({'edu_id': edu_rcd.id,
#                                  'major': edu_rcd.major,
#                                  'graduation_year': edu_rcd.graduation_year,
#                                  'edu_background': edu_rcd.background,
#                                  'school': edu_rcd.school})
#             return {'tag': OK_GET_EDU,
#                     'grade': latest_year,
#                     'edu_background': edu_background,
#                     'edu_list': edu_list}
#
#         # 如果该学生无教育经历
#         elif filter_set.count() == 0:
#             return {'tag': ERR_GET_NO_EDU}
#         # 如果该学生的教育经历数量不合法
#         else:
#             logger.error('学生id为%s的学生拥有不合法的教育经历数量，导致获取教育经历失败' % stu_id)
#             return {'tag': ERR_GET_EDU_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试获取不存在的学生的教育经历')
#         return {'tag': ERR_GET_EDU_DB}
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，查询教育经历失败')
#         return {'tag': ERR_GET_EDU_DB}
#
#
# def update_edu(stu_id, edu_id, major, graduation_year, edu_background, school):
#     """
#     修改教育经历
#     成功：返回{'tag': OK_UPDATE_EDU,
#                         'grade': get_rlt['grade'],
#                         'edu_background': get_rlt['edu_background']}
#     失败：返回{'tag': ERR_UPDATE_EDU_DB}
#     @stu_id: 学生id
#     @edu_id: 教育经历记录的id
#     @major: 专业
#     @graduation_year: 毕业年份
#     @edu_background: 学历
#     @school: 学校
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         edu_select_rlt = edu.select(edu_id)
#         if edu_select_rlt['tag'] != OK_SELECT:
#             logger.warning('尝试更新不存在的教育经历记录')
#             logger.error('获取原先的教育经历信息失败，导致更新教育经历失败')
#             return {'tag': ERR_UPDATE_EDU_DB}
#
#         pre_edu = edu_select_rlt['edu']
#
#         update_tag = \
#             edu.id_stu_update(edu_id, select_rlt['stu'], major, int(graduation_year), int(edu_background), school)
#
#         # 如果更新成功
#         if update_tag == OK_UPDATE:
#             get_rlt = get_edu(stu_id)
#             # 如果获取教育经历列表成功
#             if get_rlt['tag'] == OK_GET_EDU:
#                 return {'tag': OK_UPDATE_EDU,
#                         'grade': get_rlt['grade'],
#                         'edu_background': get_rlt['edu_background']}
#
#             # 如果获取教育经历列表失败
#             else:
#                 logger.error('数据库异常无法获取学生信息中的grade和edu_background，导致更新教育经历失败')
#                 # 回滚
#                 roll_tag = edu.update(edu_id, major=pre_edu.major, graduation_year=pre_edu.graduation_year,
#                                       background=pre_edu.background, school=pre_edu.school)
#                 if roll_tag != OK_UPDATE:
#                     logger.error("获取grade和edu_background失败，但无法恢复已更新的教育经历")
#                 return {'tag': ERR_ADD_EDU_DB}
#         # 如果更新失败
#         else:
#             return {'tag': ERR_UPDATE_EDU_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试更新不存在的学生的教育经历')
#         return {'tag': ERR_UPDATE_EDU_DB}
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，修改教育经历失败')
#         return {'tag': ERR_UPDATE_EDU_DB}
#
#
# def del_edu(stu_id, edu_id):
#     """
#     删除教育经历
#     成功：返回{'tag': OK_DEL_EDU,
#                         'grade': get_rlt['grade'],
#                         'edu_background': get_rlt['edu_background']}
#     失败：返回{'tag': ERR_DEL_EDU_DB}
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         # 保留原先的记录信息
#         edu_select_rlt = edu.select(edu_id)
#         # 如果获取原先的记录信息失败
#         if edu_select_rlt['tag'] != OK_SELECT:
#             logger.warning('尝试删除不存在的教育经历记录')
#             logger.error('获取原先的教育经历失败，导致删除教育经历失败')
#             return {'tag': ERR_DEL_EDU_DB}
#
#         # 如果获取原先的记录信息成功
#         pre_edu = edu_select_rlt['edu']
#
#         # 删除
#         del_tag = edu.id_stu_delete(edu_id=edu_id, stu=select_rlt['stu'])
#         # 如果删除成功
#         if del_tag == OK_DELETE:
#             get_rlt = get_edu(stu_id)
#             # 如果获取教育经历列表成功
#             if get_rlt['tag'] == OK_GET_EDU:
#                 return {'tag': OK_DEL_EDU,
#                         'grade': get_rlt['grade'],
#                         'edu_background': get_rlt['edu_background']}
#
#             # 如果删除后已无教育经历
#             elif get_rlt['tag'] == ERR_GET_NO_EDU:
#                 return {'tag': OK_DEL_LAST_EDU}
#
#             # 如果获取教育经历列表失败
#             else:
#                 logger.error('数据库异常无法获取学生信息中的grade和edu_background，导致删除教育经历失败')
#                 # 回滚
#                 roll_rlt = edu.id_insert(edu_id=edu_id, major=pre_edu.major, graduation_year=pre_edu.graduation_year,
#                                          background=pre_edu.background, school=pre_edu.school, stu=select_rlt['stu'])
#                 if roll_rlt['tag'] != OK_INSERT:
#                     logger.error('获取学生信息中的grade和edu_background失败，但无法恢复已删除的教育信息记录')
#                 return {'tag': ERR_DEL_EDU_DB}
#
#         # 如果删除失败
#         else:
#             return {'tag': ERR_DEL_EDU_DB}
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试删除不存在的学生的教育经历')
#         return {'tag': ERR_DEL_EDU_DB}
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，删除教育经历失败')
#         return {'tag': ERR_DEL_EDU_DB}
#
#
# def get_intern(stu_id):
#     """
#     获取学生的实习经历
#     成功：返回{'tag': OK_GET_INTERN, 'intern_list': list(filter_set.values())}
#                             "intern_list": [{
#             　　　　　　                          "intern_id": intern_id,
#             　　　　　　                          "company": company,
#             　　　　　　                          "position": position,
#             　　　　　　                          "begin_time": begin_time,
#             　　　　　　                          "end_time": end_time,
#             　　　　　　                          "description": description},
#             　　　                           ...]}
#     失败：返回{'tag': ERR_GET_NO_INTERN}
#           或{'tag': ERR_GET_INTERN_DB}
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         filter_set = intern.stu_filter(stu=select_rlt['stu'])
#
#         # 如果该学生有合法的实习经历数量
#         if filter_set.count() in range(1, 6):
#             return {'tag': OK_GET_INTERN,
#                     'intern_list': list(filter_set.values())}
#
#         # 如果该学生无实习经历
#         elif filter_set.count() == 0:
#             return {'tag': ERR_GET_NO_INTERN}
#         # 如果该学生的实习经历数量不合法
#         else:
#             logger.error('学生id为%s的学生拥有不合法的实习经历数量，导致获取实习经历失败' % stu_id)
#             return {'tag': ERR_GET_INTERN_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试获取不存在的学生的实习经历')
#         return {'tag': ERR_GET_INTERN_DB}
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，查询实习经历失败')
#         return {'tag': ERR_GET_INTERN_DB}
#
#
# def add_intern(stu_id, company, position, begin_time, end_time, description):
#     """
#     增加实习经历
#     @stu_id: 关联的学生id
#     @company: 公司
#     @position: 职位
#     @begin_time: 开始时间
#     @end_time: 结束时间
#     @description: 描述
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         # 如果实习经历未达五条
#         if intern.stu_filter(stu=select_rlt['stu']).count() < 5:
#             insert_rlt = intern.insert(company=company, position=position, begin_time=begin_time,
#                                        end_time=end_time, description=description, stu=select_rlt['stu'])
#             # 如果插入成功：
#             if insert_rlt['tag'] == OK_INSERT:
#                 return {'tag': OK_ADD_INTERN,
#                         'intern_id': insert_rlt['intern'].intern_id}
#             # 如果插入失败（insert_rlt['tag'] == ERR_INSERT_DB）
#             else:
#                 return {'tag': ERR_ADD_INTERN_DB}
#         # 如果实习经历已有五条或更多
#         else:
#             return {'tag': ERR_ADD_INTERN_FULL}
#
#     # 如果学生记录不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试为不存在的学生增加实习经历')
#         return {'tag': ERR_ADD_INTERN_DB}
#     # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，增加实习经历失败')
#         return {'tag': ERR_ADD_INTERN_DB}
#
#
# def update_intern(intern_id, stu_id, company, position, begin_time, end_time, description):
#     """
#     修改实习经历
#     成功：返回{'tag': OK_UPDATE_INTERN}
#     失败：返回{'tag': ERR_UPDATE_INTERN_DB}
#     @intern_id: 实习记录的id
#     @stu_id:  关联的学生id
#     @company: 公司
#     @position: 职位
#     @begin_time: 开始时间
#     @end_time:  结束时间
#     @description:  描述
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         update_tag = \
#             intern.id_stu_update(intern_id, select_rlt['stu'], company, position, begin_time, end_time, description)
#
#         # 如果更新成功
#         if update_tag == OK_UPDATE:
#             return {'tag': OK_UPDATE_INTERN}
#         # 如果更新失败
#         else:
#             return {'tag': ERR_UPDATE_INTERN_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试更新不存在的学生的实习经历')
#         return {'tag': ERR_UPDATE_INTERN_DB}
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，修改实习经历失败')
#         return {'tag': ERR_UPDATE_INTERN_DB}
#
#
# def del_intern(stu_id, intern_id):
#     """
#     删除实习经历
#     成功：返回{'tag': OK_DEL_INTERN}
#     失败：返回{'tag': ERR_DEL_INTERN_DB}
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         delete_tag = intern.id_stu_delete(intern_id, select_rlt['stu'])
#         if delete_tag == OK_DELETE:
#             return {'tag': OK_DEL_INTERN}
#
#         # delete_tag == ERR_DELETE_DB
#         else:
#             return {'tag': ERR_DEL_INTERN_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试删除不存在的学生的实习经历')
#         return {'tag': ERR_DEL_INTERN_DB}
#
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，删除实习经历失败')
#         return {'tag': ERR_DEL_INTERN_DB}
#
#
# def get_proj(stu_id):
#     """
#     获取项目经历
#     成功：返回{'tag': OK_GET_PROJ, 'proj_list': list(filter_set.values())}
#                             "proj_list": [{
#             　　　　　　                      "proj_id": proj_id,
#             　　　　　　                      "name": name,
#             　　　　　　                      "duty": duty,
#             　　　　　　                      "year": year,
#             　　　　　　                      "description": description},
#             　　　                         ...]}
#     失败：返回{'tag': ERR_GET_NO_PROJ}
#           或{'tag': ERR_GET_PROJ_DB}
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         filter_set = proj.stu_filter(stu=select_rlt['stu'])
#
#         # 如果该学生有合法的项目经历数量
#         if filter_set.count() in range(1, 6):
#             return {'tag': OK_GET_PROJ,
#                     'proj_list': list(filter_set.values())}
#
#         # 如果该学生无项目经历
#         elif filter_set.count() == 0:
#             return {'tag': ERR_GET_NO_PROJ}
#         # 如果该学生的实习经历数量不合法
#         else:
#             logger.error('学生id为%s的学生拥有不合法的项目经历数量，导致获取项目经历失败' % stu_id)
#             return {'tag': ERR_GET_PROJ_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试获取不存在的学生的项目经历')
#         return {'tag': ERR_GET_PROJ_DB}
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，查询项目经历失败')
#         return {'tag': ERR_GET_PROJ_DB}
#
#
# def add_proj(stu_id, name, duty, year, description):
#     """
#     增加项目经历
#     成功：返回{'tag': OK_ADD_PROJ, 'proj_id': insert_rlt['proj'].proj_id}
#     失败：返回{'tag': ERR_ADD_PROJ_DB}或{'tag': ERR_ADD_PROJ_FULL}
#     @stu_id:关联的学生id
#     @name: 项目名称
#     @duty: 职责
#     @year: 年份
#     @description: 描述
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         # 如果项目经历未达五条
#         if proj.stu_filter(stu=select_rlt['stu']).count() < 5:
#             insert_rlt = \
#                 proj.insert(name=name, duty=duty, year=year, description=description, stu=select_rlt['stu'])
#             # 如果插入成功：
#             if insert_rlt['tag'] == OK_INSERT:
#                 return {'tag': OK_ADD_PROJ,
#                         'proj_id': insert_rlt['proj'].proj_id}
#             # 如果插入失败（insert_rlt['tag'] == ERR_INSERT_DB）
#             else:
#                 return {'tag': ERR_ADD_PROJ_DB}
#         # 如果实习经历已有五条或更多
#         else:
#             return {'tag': ERR_ADD_PROJ_FULL}
#
#     # 如果学生记录不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试为不存在的学生增加项目经历')
#         return {'tag': ERR_ADD_PROJ_DB}
#     # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，增加项目经历失败')
#         return {'tag': ERR_ADD_PROJ_DB}
#
#
# def update_proj(proj_id, stu_id, name, duty, year, description):
#     """
#     修改项目经历
#     成功：返回{'tag': OK_UPDATE_PROJ}
#     失败：返回{'tag': ERR_UPDATE_PROJ_DB}
#     @proj_id: 项目记录的id
#     @stu_id:  关联的学生id
#     @name: 项目名称
#     @duty: 职责
#     @year: 年份
#     @description:  描述
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         update_tag = \
#             proj.id_stu_update(proj_id, select_rlt['stu'], name, duty, year, description)
#
#         # 如果更新成功
#         if update_tag == OK_UPDATE:
#             return {'tag': OK_UPDATE_PROJ}
#         # 如果更新失败
#         else:
#             return {'tag': ERR_UPDATE_PROJ_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试更新不存在的学生的项目经历')
#         return {'tag': ERR_UPDATE_PROJ_DB}
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，修改项目经历失败')
#         return {'tag': ERR_UPDATE_PROJ_DB}
#
#
# def del_proj(stu_id, proj_id):
#     """
#     删除项目经历
#     成功：返回{'tag': OK_DEL_PROJ}
#     失败：返回{'tag': ERR_DEL_PROJ_DB}
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         delete_tag = proj.id_stu_delete(proj_id, select_rlt['stu'])
#         if delete_tag == OK_DELETE:
#             return {'tag': OK_DEL_PROJ}
#
#         # delete_tag == ERR_DELETE_DB
#         else:
#             return {'tag': ERR_DEL_PROJ_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试删除不存在的学生的项目经历')
#         return {'tag': ERR_DEL_PROJ_DB}
#
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，删除项目经历失败')
#         return {'tag': ERR_DEL_PROJ_DB}


# def upload_works(stu_id, works):
#     """
#     上传作品集文件
#     @stu_id 学生id
#     @works: 作品集文件
#     成功：返回{'tag': OK_SAVE_WORKS, 'path': ref_path}
#     失败：返回{'tag': ERR_SAVE_WORKS_FAIL}
#     """
#
#     def check_resume_file(file):  # TODO(hjf): Check works file
#         """return true if works file is valid"""
#         return True
#
#     def get_works_path(folder, file_name, file_type):
#         return '%s/%s/%s.%s' % (WORKS_PATH_ROOT, folder, file_name, file_type)
#
#     # 确认学生是否存在
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         # 如果作品集文件合法
#         if check_resume_file(works):
#             works_path = get_works_path(folder=stu_id,
#                                         file_name=int(time.time()),
#                                         file_type=file_helper.get_file_type(works.name))  # 用time作简历文件名称
#             # ref_path = '/media/' + works_path
#             ref_path = works_path
#
#             # 如果作品集文件上传成功
#             if file_helper.save(works, works_path):
#                 return {'tag': OK_SAVE_WORKS,
#                         'path': ref_path}
#             # 如果作品集文件上传失败，
#             else:
#                 return {'tag': ERR_SAVE_WORKS_FAIL}
#
#         # 如果作品集文件不合法
#         else:
#             return {'tag': ERR_WORKS_FILE_INVALID}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试为不存在的学生上传作品集')
#         return {'tag': ERR_SAVE_WORKS_FAIL}
#     # 如果数据库异常导致查询学生是否存在失败(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确定学生是否存在，上传作品集失败')
#         return {'tag': ERR_SAVE_WORKS_FAIL}
#
#
# def add_works(stu_id, path, site):
#     """
#     增加作品集信息
#     成功：返回{'tag': OK_ADD_WORKS, 'works_id': insert_rlt['works'].works_id}
#     失败：返回{'tag': ERR_ADD_WORKS_DB}或{'tag': ERR_ADD_WORKS_EXIST}
#     @stu_id:关联的学生id
#     @path: 作品集路径
#     @site: 作品集在线网址
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         works_select_rlt = works.stu_select(stu=select_rlt['stu'])
#         # 如果还没有作品集信息
#         if works_select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#             insert_rlt = \
#                 works.insert(path=path, site=site, stu=select_rlt['stu'])
#             # 如果插入成功：
#             if insert_rlt['tag'] == OK_INSERT:
#                 return {'tag': OK_ADD_WORKS,
#                         'works_id': insert_rlt['works'].works_id}
#             # 如果插入失败（insert_rlt['tag'] == ERR_INSERT_DB）
#             else:
#                 return {'tag': ERR_ADD_WORKS_DB}
#         # 如果已有作品集信息
#         elif works_select_rlt['tag'] == OK_SELECT:
#             return {'tag': ERR_ADD_WORKS_EXIST}
#         # 如果数据库异常导致无法确认是否已有作品集
#         else:
#             logger.error('数据库异常导致无法确认学生是否存在，增加作品集信息失败')
#             return {'tag': ERR_ADD_WORKS_DB}
#
#     # 如果学生记录不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试为不存在的学生增加作品集信息')
#         return {'tag': ERR_ADD_WORKS_DB}
#     # 如果数据库异常导致获取学生信息失败(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，增加作品集信息失败')
#         return {'tag': ERR_ADD_WORKS_DB}
#
#
# def update_works(works_id, stu_id, path, site):
#     """
#     修改作品集信息
#     成功：返回{'tag': OK_UPDATE_WORKS}
#     失败：返回{'tag': ERR_UPDATE_WORKS_DB}
#     @works_id: 技能评价的id
#     @stu_id:  关联的学生id
#     @path: 路径
#     @site: 作品集的在线网址
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         update_tag = \
#             works.id_stu_update(works_id, select_rlt['stu'], path, site)
#
#         # 如果更新成功
#         if update_tag == OK_UPDATE:
#             return {'tag': OK_UPDATE_WORKS}
#         # 如果更新失败
#         else:
#             return {'tag': ERR_UPDATE_WORKS_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试更新不存在的学生的作品集信息')
#         return {'tag': ERR_UPDATE_WORKS_DB}
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，修改作品集信息失败')
#         return {'tag': ERR_UPDATE_WORKS_DB}
#
#
# def del_works(stu_id, works_id):
#     """
#     删除作品集信息
#     成功：返回{'tag': OK_DEL_WORKS}
#     失败：返回{'tag': ERR_DEL_WORKS_DB}
#     """
#     select_rlt = stu_info.select(stu_id=stu_id)
#     # 如果学生存在
#     if select_rlt['tag'] == OK_SELECT:
#         delete_tag = works.id_stu_delete(works_id, select_rlt['stu'])
#         if delete_tag == OK_DELETE:
#             return {'tag': OK_DEL_WORKS}
#
#         # delete_tag == ERR_DELETE_DB
#         else:
#             return {'tag': ERR_DEL_WORKS_DB}
#
#     # 如果学生不存在
#     elif select_rlt['tag'] == ERR_SELECT_NOTEXIST:
#         logger.warning('尝试删除不存在的学生的作品集信息')
#         return {'tag': ERR_DEL_WORKS_DB}
#
#     # 如果数据库异常导致无法确认学生是否存在(select_rlt['tag'] == ERR_SELECT_DB)
#     else:
#         logger.error('数据库异常导致无法确认学生是否存在，删除作品集信息失败')
#         return {'tag': ERR_DEL_WORKS_DB}










