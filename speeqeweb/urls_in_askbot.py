from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^virtualhost/(?P<virtual_name>[\w|\@|\_|:|\+|&|\-|#|\.]+)/','askbot.deps.speeqeweb.speeqe.views.client'),
    (r'^room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','askbot.deps.speeqeweb.speeqe.views.client'),
    (r'^client/room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','askbot.deps.speeqeweb.speeqe.views.client'),
    (r'^client/','askbot.deps.speeqeweb.speeqe.views.client'),
    (r'^$','speeqeweb.speeqe.views.index'),
)

if settings.SERVE_STATIC_URLS:
    urlpatterns += patterns('',
                            (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DOCUMENT_ROOT }),
                            )