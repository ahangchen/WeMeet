from django.conf.urls import url
from team import views

urlpatterns = [
    url(r'^$', views.test, name='index'),
    url(r'^valid_code/$', views.valid_code),
]