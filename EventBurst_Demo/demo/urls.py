#mydemo/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),# local host/demo 根目录是到views.index下
    #url('themeriver',views.themeriver,name="theamriver"),
    url('test',views.test,name="test"),
    url('event_chain',views.event_chain,name="event_chain"),
    url('event',views.event,name="event")
]