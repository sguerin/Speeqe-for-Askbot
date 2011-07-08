from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    # comment if login method is askbot
    (r'^join/validate/username/','speeqeweb.speeqe.views.validate_username'),
    (r'^join/validate/email/','speeqeweb.speeqe.views.validate_email'),
    (r'^join/','speeqeweb.speeqe.views.join'),
    (r'^accounts/signin/$', 'speeqeweb.speeqe.views.login'),
    (r'^accounts/signout/$', 'django.contrib.auth.views.logout'),

    # needed
    (r'^virtualhost/(?P<virtual_name>[\w|\@|\_|:|\+|&|\-|#|\.]+)/','speeqeweb.speeqe.views.client'),
    (r'^room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','speeqeweb.speeqe.views.client'),
    (r'^client/room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','speeqeweb.speeqe.views.client'),
    (r'^client/','speeqeweb.speeqe.views.client'),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^$','speeqeweb.speeqe.views.index'),

)

if settings.SERVE_STATIC_URLS:
    urlpatterns += patterns('',
                            (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DOCUMENT_ROOT }),
                            )
