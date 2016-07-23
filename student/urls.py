from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^activate/(.+)/$', views.activate),
    url(r'^login/$', views.login),
    url(r'^rsmail/$', views.send_rsmail),  # rsmail: reset mail
    url(r'^reset/$', views.reset),
    url(r'^cpwd/$', views.change_pwd),  # cpwd: change password
    url(r'^info/get/$', views.get_info),
    url(r'^info/avatar/$', views.save_avatar),
    url(r'^info/update/$', views.update_info),
    url(r'^fetch/$', views.fetch),  # render reset page
    url(r'^resume/upload/$', views.upload_resume),
    url(r'^resume/apply/$', views.job_apply),
    url(r'^info/edu/add/$', views.add_edu),
    url(r'^info/edu/get/$', views.get_edu),
    url(r'^info/intern/get/$', views.get_intern),
    url(r'^$', views.post),
]
