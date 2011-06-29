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


#SESSION_COOKIE_DOMAIN = ".murex.com"

#type of database you want to use for django
DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'speeqe'             # Or path to database file if using sqlite3.
DATABASE_USER = 'speeqe'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

#where all your media , intended to be served via django, lives
MEDIA_ROOT = '/var/www/speeqeweb/webroot'
#where all your static documents are.
DOCUMENT_ROOT = '/var/www/speeqeweb/webroot'

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

#multi user chat rooms listed on the front page.  This list contains
#the rooms that will be displayed on the speeqe web pages. The first
#entry is the title, followed by the room url.  You can use /room/ or
#the dns trick if you have that setup.
FEATURED_ROOMS =  {'ore':'/room/ore/', 'mad':'/room/mad/', }

#where all your django templates live.  make sure to have the location
#of your themes and client.html, test_client.html in this config
#option
TEMPLATE_DIRS = (
    '/var/www/speeqe/speeqeweb/templates',
    '/lib/python/speeqeweb/templates',    
    '/var/www/speeqe/speeqeweb/webroot',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

#mail server used to send email
SMTP_SERVER = 'smtp.tribe.com'
#username and password if using smtp auth
SMTP_USERNAME = ''
SMTP_PASSWORD = ''
SMTP_PORT = 2525
#email used when someone clicks on a help email link
HELP_EMAIL = 'admin@tribe.com'

#default sha1 for your default avatar image
AVATAR_DEFAULT_SHA1 = 'f2f8ab835b10d66f9233518d1047f3014b3857cf'
#default avatar sha1 when an IE6 user comes to the website
AVATAR_DEFAULT_IE6 = 'b04b0e215af8ce2b7d620aaef32492c8bfc06ed5'
#change the size of the images returned. first is height, followed by width.
AVATAR_DEFAULT_DIMENSIONS = '30|30'
#the amount of time the image is cached
AVATAR_CACHE_TIMEOUT = 6000

#allows django to serve all unknown urls as static data
SERVE_STATIC_URLS = True
#tells speeqe that you have the dns trick configured. (ie. you can use
#http://roomname.yourdomain.com). False if dns names are not configured.
DNS_ROOM_NAMES = False
