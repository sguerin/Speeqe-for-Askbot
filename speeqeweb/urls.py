from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^avatar-service/',   include('speeqeweb.avatars.urls')),
    (r'^join/validate/username/','speeqeweb.speeqe.views.validate_username'),
    (r'^join/validate/email/','speeqeweb.speeqe.views.validate_email'),
    (r'^join/','speeqeweb.speeqe.views.join'),
    (r'^virtualhost/(?P<virtual_name>[\w|\@|\_|:|\+|&|\-|#|\.]+)/','speeqeweb.speeqe.views.client'),
    (r'^room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','speeqeweb.speeqe.views.client'),
    (r'^client/room/(?P<room_name>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/','speeqeweb.speeqe.views.client'),
    (r'^client/','speeqeweb.speeqe.views.client'),
    (r'^accounts/login/$', 'speeqeweb.speeqe.views.login'),
    (r'^accounts/ajax_login/$', 'speeqeweb.speeqe.views.ajax_login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^messagesearch/(?P<room>[\w|\@|\.|\_|:|\+|&|\-|%|#]+)/', 'speeqeweb.speeqe.views.room_message_search'),   
    (r'^messagesearch/$', 'speeqeweb.speeqe.views.room_message_search'),
    (r'^themes/new/$', 'speeqeweb.speeqe.views.new_theme'),
    (r'^themes/edit/(?P<theme_id>\d+)/', 'speeqeweb.speeqe.views.edit_theme'),
    (r'^themes/link/', 'speeqeweb.speeqe.views.link_theme_to_room'),
    (r'^themes/$', 'speeqeweb.speeqe.views.list_themes'),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^$','speeqeweb.speeqe.views.index'),

)

if settings.SERVE_STATIC_URLS:
    urlpatterns += patterns('',
                            (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.DOCUMENT_ROOT }),
                            )
