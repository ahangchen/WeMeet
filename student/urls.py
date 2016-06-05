from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^register/$', views.register_stu),
    url(r'^update/$', views.update_stu_info),
    url(r'^information/$', views.get_stu_info),
    url(r'^$', views.post),
]