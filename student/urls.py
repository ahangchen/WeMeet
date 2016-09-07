from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^activate/(.+)/$', views.activate),
    url(r'^login/$', views.login),
    url(r'^rsmail/$', views.send_rsmail),  # rsmail: reset mail
    url(r'^fetch/$', views.fetch),
    url(r'^reset/$', views.reset),
    url(r'^cpwd/$', views.change_pwd),  # cpwd: change password
    url(r'^info/get/$', views.get_info),
    url(r'^info/avatar/$', views.save_avatar),
    url(r'^info/update/$', views.update_info),
    url(r'^fetch/$', views.fetch),  # render reset page
    url(r'^resume/upload/$', views.upload_resume),
    url(r'^resume/apply/$', views.job_apply),
    url(r'^resume/get/$', views.get_resume),
    url(r'^resume/del/$', views.del_resume),
    url(r'^info/edu/add/$', views.add_edu),
    url(r'^info/edu/get/$', views.get_edu),
    url(r'^info/edu/update/$', views.update_edu),
    url(r'^info/edu/del/$', views.del_edu),
    url(r'^info/intern/add/$', views.add_intern),
    url(r'^info/intern/get/$', views.get_intern),
    url(r'^info/intern/update/$', views.update_intern),
    url(r'^info/intern/del/$', views.del_intern),
    url(r'^info/proj/add/$', views.add_proj),
    url(r'^info/proj/get/$', views.get_proj),
    url(r'^info/proj/update/$', views.update_proj),
    url(r'^info/proj/del/$', views.del_proj),
    url(r'^info/works/get/$', views.get_works),
    url(r'^info/works/add/$', views.add_works),
    url(r'^info/works/upload/$', views.upload_works),
    url(r'^info/works/update/$', views.update_works),
    url(r'^info/works/del/$', views.del_works),
    url(r'^info/skill/get/$', views.get_skill),
    url(r'^info/skill/add/$', views.add_skill),
    url(r'^info/skill/update/$', views.update_skill),
    url(r'^info/skill/del/$', views.del_skill),
    url(r'^apply/list/$', views.stu_get_apply),
    url(r'^apply/read/$', views.set_apply_read),
    url(r'^$', views.post),
]
