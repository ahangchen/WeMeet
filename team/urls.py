from django.conf.urls import url
from team import views

urlpatterns = [
    url(r'^$', views.test, name='index'),
    url(r'^valid_code/$', views.valid_code),
    url(r'^test/$', views.test),
    url(r'^search/$', views.search),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^reset/$', views.reset),
    url(r'^fetch/$', views.fetch),
    url(r'^update_pwd/$', views.update_pwd),
]