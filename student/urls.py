from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^activate/(.+)/$', views.activate),
    url(r'^login/$', views.login),
    url(r'^rsmail/$', views.send_rsmail),  # rsmail: reset mail
    url(r'^reset/$', views.reset),
    url(r'^cpwd/$', views.change_pwd),  # cpwd: change password
    url(r'^info/$', views.get_info),
    url(r'^info/avatar/$', views.save_avatar),
    url(r'^info/update/$', views.update_info),
    url(r'^reset_page/(.+)', views.reset_page),  # render reset page
    url(r'^$', views.post),
]
