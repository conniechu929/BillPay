from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout),
    url(r'^bills$', views.bills),
    url(r'^newbill$', views.addBill),
    url(r'^markbill/(?P<id>\d+)$', views.markBill),
    url(r'^searchDate$', views.searchDate),
    url(r'^deletebill/(?P<id>\d+)$', views.deleteBill),
    url(r'^update_bill/(?P<id>\d+)$', views.updateBill),
]
