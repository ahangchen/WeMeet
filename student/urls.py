from django.conf.urls import url


urlpatterns = [
    url(r'^insert_page/$', 'student.views.insert_page'),
    url(r'^insert/$', 'student.views.insert'),
    url(r'^delete_page/$', 'student.views.delete_page'),
    url(r'^delete/$', 'student.views.delete'),
    url(r'^update_page/$', 'student.views.update_page'),
    url(r'^update/$', 'student.views.update'),
    url(r'^select_page/$', 'student.views.select_page'),
    url(r'^select/$', 'student.views.select'),
    url(r'^show_all/$', 'student.views.show_all'),

]