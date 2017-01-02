CREATE DATABASE wemeet;

create user wemeet@localhost identified by 'wmms233';
grant all *.* to 'wemeet'@'localhost';
create database wemeet;
ALTER TABLE auth_group CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_group_permissions CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_permission CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_user CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_user_groups CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE auth_user_user_permissions CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE django_admin_log CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE django_content_type CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE django_migrations CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE django_session CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE job_apply CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE stu_account CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE stu_edu CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE stu_info CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE stu_intern CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE stu_intern CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE stu_proj CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE stu_skill CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE stu_works CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_businesstype CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_job CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_jobtype CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_label CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_product CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_pwd CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_team CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_teamimg CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_teamstu CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_teamtype CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE team_worktype CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;

insert into team_jobtype (name) values ('行政');
insert into team_jobtype (name) values ('产品');
insert into team_jobtype (name) values ('技术');
insert into team_jobtype (name) values ('设计');
insert into team_jobtype (name) values ('运营');
insert into team_jobtype (name) values ('运维支持');
insert into team_jobtype (name) values ('市场');
insert into team_jobtype (name) values ('文案策划');
insert into team_jobtype (name) values ('营销');


insert into team_businesstype (name) values ('校园服务');
insert into team_businesstype (name) values ('O2O');
insert into team_businesstype (name) values ('移动互联网');
insert into team_businesstype (name) values ('电子商务');
insert into team_businesstype (name) values ('医疗健康');
insert into team_businesstype (name) values ('金融');
insert into team_businesstype (name) values ('法务');
insert into team_businesstype (name) values ('咨询');
insert into team_businesstype (name) values ('数据安全');
insert into team_businesstype (name) values ('文化娱乐');
insert into team_businesstype (name) values ('食品化工');
insert into team_businesstype (name) values ('广告营销');
insert into team_businesstype (name) values ('游戏');
insert into team_businesstype (name) values ('招聘');
insert into team_businesstype (name) values ('教育');
insert into team_businesstype (name) values ('旅游');
insert into team_businesstype (name) values ('社交网络');
insert into team_businesstype (name) values ('硬件');
insert into team_businesstype (name) values ('分类信息');
insert into team_businesstype (name) values ('生活服务');
insert into team_businesstype (name) values ('其他');

update stu_info set year=1995, month='12', school='华南理工大学', major='软件工程', location='广州', tel='18813299013' where id = 2;
update stu_info set sex=1, name='张铭杰' where id = 2;
update stu_info set year=1993, month='12', school='华南理工大学', major='软件工程', location='广州', tel='18813299013' where id = 1;
update stu_info set sex=1, name='陈伟航' where id = 1;
