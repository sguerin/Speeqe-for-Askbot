from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^virtualhost/(?P<virtual_name>[\w|\@|\_|:|\+|&|\-|#|\.]+)/','speeqeweb.speeqe.views.client'),
    (r'^room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','speeqeweb.speeqe.views.client'),
    (r'^client/room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','speeqeweb.speeqe.views.client'),
    (r'^client/','speeqeweb.speeqe.views.client'),
    (r'^$','speeqeweb.speeqe.views.index'),
)