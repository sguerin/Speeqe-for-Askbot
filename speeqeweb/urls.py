from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    # comment if login method is askbot
    (r'^join/validate/username/','speeqeweb.speeqe.views.validate_username'),
    (r'^join/validate/email/','speeqeweb.speeqe.views.validate_email'),
    (r'^join/','speeqeweb.speeqe.views.join'),
    (r'^account/signin/$', 'speeqeweb.speeqe.views.login'),
    (r'^account/signout/$', 'django.contrib.auth.views.logout'),

    # needed
    (r'^chat/virtualhost/(?P<virtual_name>[\w|\@|\_|:|\+|&|\-|#|\.]+)/','speeqeweb.speeqe.views.client'),
    (r'^chat/room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','speeqeweb.speeqe.views.client'),
    (r'^chat/client/room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','speeqeweb.speeqe.views.client'),
    (r'^chat/client/','speeqeweb.speeqe.views.client'),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^chat/$','speeqeweb.speeqe.views.index'),
    (r'^$','speeqeweb.speeqe.views.index'),
)