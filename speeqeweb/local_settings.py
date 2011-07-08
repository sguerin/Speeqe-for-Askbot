#Domain for your website
#HTTP_DOMAIN is used to build the login url and also the username ...
HTTP_DOMAIN = "tribe"
#Domain for your jabber server
XMPP_DOMAIN = "tribe"

#names you dont want your users to have. When signing up for an
#account and the user name is one of these exact words, it will be
#rejected.
EXACT_BAD_WORDS = ['crap']
#words you don't want in your user's names.  When signing up for an
#account and the username has one of these words in it, the name will
#be rejected.
MATCH_BAD_WORDS = ['crap'] 

#where all your static documents are.
DOCUMENT_ROOT = '/var/www/speeqe/speeqeweb/webroot'
#DOCUMENT_ROOT = '/usr/local/virtualenv/askbot/lib/python2.6/site-packages/askbot/deps/speeqeweb/webroot'

#the user used to list active rooms on the website. the speeqe website
#needs a user and password to connect and run disco requests. This is
#to gather a list of active rooms from the muc component.
XMPP_USER = ''
XMPP_PASS = ''
#your multi user chat server name. used to gather a list of active rooms
XMPP_CHAT = 'conference.tribe.com'
#the name of your bosh server. Bosh is used to authenticate users to
#the website and then they are auto logged in to each chat room.
BOSH_HOST = "tribe.com"
#the port your bosh server listens on
BOSH_PORT = "7070"
#the url used to proxy to your bosh server
BOSH_URL = "/http-bind"

#multi user chat rooms listed in first on the front page.
#The rooms must exist in teh server to be displayed.
#entry is the title, followed by the room url.  You can use /room/ or
#the dns trick if you have that setup.
#since the room must exist, the room url is not used anymore.
FEATURED_ROOMS =  {'ore':'/room/ore/', 'mad':'/room/mad/', }

#where all your django templates live.  make sure to have the location
#of your themes and client.html, test_client.html in this config
#option
TEMPLATE_DIRS = (
    '/var/www/speeqe/speeqeweb/templates',
    '/var/www/speeqe/speeqeweb/webroot',
    '/usr/local/virtualenv/askbot/lib/python2.6/site-packages/askbot/deps/speeqeweb/webroot',
    '/usr/local/virtualenv/askbot/lib/python2.6/site-packages/askbot/deps/speeqeweb/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#allows django to serve all unknown urls as static data
SERVE_STATIC_URLS = True
#tells speeqe that you have the dns trick configured. (ie. you can use
#http://roomname.yourdomain.com). False if dns names are not configured.
DNS_ROOM_NAMES = False
