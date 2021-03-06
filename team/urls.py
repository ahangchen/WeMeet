from django.conf.urls import url

from team import views
from team import ctrl
from team.api import topic, job, product, account, apply, team, search
from team.ctrl import focus

focusjob_list = focus.FocusJobList.as_view({
    'get': 'list',
    'post': 'create'
})

focusjob_detail = focus.FocusJobList.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

focusteam_list = focus.FocusTeamList.as_view({
    'get': 'list',
    'post': 'create'
})

focusteam_detail = focus.FocusTeamList.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

focusstu_list = focus.FocusStuList.as_view({
    'get': 'list',
    'post': 'create'
})

focusstu_detail = focus.FocusStuList.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = [
    url(r'^$', views.test, name='index'),
    url(r'^valid_code/$', views.valid_code),
    url(r'^test/$', views.test),
    url(r'^search/$', search.search),
    url(r'^hot_product/$', search.hot_product),
    url(r'^hot_team/$', search.hot_team),
    url(r'^search_job/$', job.search_job),
    url(r'^add_job/$', job.add_job),
    url(r'^update_job/$', job.update_job),
    url(r'^delete_job/$', job.delete_job),
    url(r'^job_type/$', job.job_type),
    url(r'^product/save_img/$', product.save_prod_img),
    url(r'^product/insert/$', product.add_product),
    url(r'^product/update/$', product.update_product),
    url(r'^product/delete/$', product.delete_product),
    url(r'^product/info/$', product.info_product),
    url(r'^product/search/$', product.search_product),
    url(r'^register/$', account.register),
    url(r'^login/$', account.login),
    url(r'^reset/$', account.reset),
    url(r'^fetch/$', account.fetch),
    url(r'^update_pwd/$', account.update_pwd),
    url(r'^job_info/$', job.job_info),
    url(r'^info/$', team.info),
    url(r'^invite/$', account.invite),
    url(r'^update_team_info/$', team.update_team_info),
    url(r'^upload_logo/$', team.upload_logo),
    url(r'^add_team_label/$', team.add_team_label),
    url(r'^rm_team_label/$', team.rm_team_label),
    url(r'^rm_team_stu/$', team.rm_team_stu),
    url(r'^add_team_stu/$', team.add_team_stu),
    url(r'^add_team_photo/$', team.add_team_photo),
    url(r'^rm_team_photo/$', team.rm_team_photo),
    url(r'^update_team_contact/$', team.update_team_contact),
    url(r'^business/$', team.business),
    url(r'^name2mail/$', team.name2mail),
    url(r'^invite_stu/$', team.invite_stu),
    url(r'^apply/list/$', apply.get_apply_list),
    url(r'^apply/info/$', apply.get_apply_info),
    url(r'^apply/mail/$', apply.apply_mail),
    url(r'^apply/handle/$', apply.apply_handle),
    url(r'^all/newest$', search.newest),
    url(r'^team/newest$', search.newest_teams),
    url(r'^V1.0/product/(?P<pk>[0-9]+)/$', ctrl.product.ProductDetail.as_view()),
    url(r'^V1.0/product/$', ctrl.product.ProductList.as_view()),
    url(r'^V1.0/product/img/$', product.save_prod_img),
    url(r'^V1.0/job/(?P<pk>[0-9]+)/$', ctrl.job.JobDetail.as_view()),
    url(r'^V1.0/job/$', ctrl.job.JobList.as_view()),
    url(r'^V1.0/job/type/$', job.job_type),
    url(r'^topic/new/$', topic.new),
    url(r'^topic/update/$', topic.update),
    url(r'^topic/remove/$', topic.remove),
    url(r'^topic/info/$', topic.info),
    url(r'^topic/list/$', topic.list),
    url(r'^focus/job/$', focusjob_list),
    url(r'^focus/job/(?P<pk>[0-9]+)/$', focusjob_detail),
    url(r'^focus/team/$', focusteam_list),
    url(r'^focus/team/(?P<pk>[0-9]+)/$', focusteam_detail),
    url(r'^focus/student/$', focusstu_list),
    url(r'^focus/student/(?P<pk>[0-9]+)/$', focusstu_detail),
    url(r'^topic/newest/$', search.newest_topic)
]
