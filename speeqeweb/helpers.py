#
# Copyright (c) 2005 - 2008 Nathan Zorn, OGG, LLC 
# See LICENSE.txt for details
#

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
import smtplib
from email.mime.text import MIMEText
import random
import string

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

def generate_code(length):
    """generate random/uniq string for confirmation codes. """
    
    we_dont_want = ['1','L','l','0','o','O']
    lowers = [a for a in string.ascii_lowercase if a not in we_dont_want]
    digits = [a for a in string.digits if a not in we_dont_want]
    password = ''
    for c in xrange(0, length):
        possible = lowers

        if c == 2 or c == 3:
            possible = digits

        password = password + random.choice(possible)
    return password

