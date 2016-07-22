from django.conf.urls import url
from team import views

urlpatterns = [
    url(r'^$', views.test, name='index'),
    url(r'^valid_code/$', views.valid_code),
    url(r'^test/$', views.test),
    url(r'^search/$', views.search),
    url(r'^hot_product/$', views.hot_product),
    url(r'^hot_team/$', views.hot_team),
    url(r'^search_job/$', views.search_job),
    url(r'^add_job/$', views.add_job),
    url(r'^update_job/$', views.update_job),
    url(r'^delete_job/$', views.delete_job),
    url(r'^job_type/$', views.job_type),
    url(r'^product/save_img/$', views.save_prod_img),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^reset/$', views.reset),
    url(r'^fetch/$', views.fetch),
    url(r'^update_pwd/$', views.update_pwd),
    url(r'^job_info/$', views.job_info),
    url(r'^info/$', views.info),
    url(r'^invite/$', views.invite)
]