# WeMeet

> 连接创业团队和学有余力的学生的校内招聘平台

## 角色
### 创业团队（扩展为社团，企业）
- 注册团队
  - 团队信息（Team_info CRUD）
    - team_id, team_name, team_manager, team_desc, team_tel, team_mail
- 发布职位需求（Job_info CRUD）
  - job_stat, job_valid_time, job_cnt, job_team, job_type
    job_title, job_desc, job_attach_path, attach_stu

- 浏览人才（需要实现条件查询，后期要有模糊匹配）

### 学生
 - 个人信息(stu_info CRUD)
   - stu_id, stu_name, stu_tel, stu_mail, stu_want, resume_path, my_meet
 - 浏览职位
 - 投递建立 

### 管理员（待定）

## 独立于角色的功能
### 通信机制
私信数据库（From, to, content, job, team）

### 登录机制
基于华工邮箱？或者普通邮箱认证？

