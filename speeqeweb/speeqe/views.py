#
# Copyright (c) 2005 - 2008 Nathan Zorn, OGG, LLC 
# See LICENSE.txt for details
#

from speeqeweb.speeqe.forms import RegisterForm
import speeqeweb.speeqe.forms
from speeqeweb.helpers import render_response, generate_code
from speeqeweb.httpbclient import PunjabClient
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.conf import settings
import datetime
import socket,random,string
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.template import Context, Template
import speeqeweb.speeqe.xmppy as xmpp

class NoSession(Exception):
	pass

def index(request):
	context = {}

	index_template = "index.html"
	
	if request.user.is_anonymous():
		request.session.set_test_cookie()
	
	return render_response(request, index_template,context)

def validate_username(request):
	"""Used to validate a username via ajax."""
	
	username = request.GET.get('username',None)
	response_string = "<username msg=''>invalid</username>"
	valid = False
	try:
		if username:
			speeqeweb.speeqe.forms.validate_username(username)
			valid = True
	except Exception,ex:
		response_string = "<username msg=\""+str(ex)+"\">invalid</username>"
	if valid:
		response_string = "<username msg=''>valid</username>"
	return HttpResponse(response_string)

def validate_email(request):
	"""Used to validate an email via ajax."""
	
	email = request.GET.get('email',None)
	response_string = "<email msg=''>invalid</email>"
	valid = False
	try:
		if email:
			speeqeweb.speeqe.forms.validate_email(email)
			valid = True
	except Exception,ex:
		response_string = "<email msg=\""+str(ex)+"\">invalid</email>"
	if valid:
		response_string = "<email msg=''>valid</email>"
	return HttpResponse(response_string)		


def join(request):
	
	"""create a speeqe account"""
	context = {}
	if request.method == "POST":
		#create a register form to handle validation and errors
		register_form = RegisterForm(request.POST)
		context={'form':register_form}
		if register_form.is_valid():
			#create the account
			new_member = register_form.save()

			username = new_member.username + "@" + new_member.realm
			user = auth.authenticate(username=username,
						 password=new_member.password)
			request.session['user_password']= register_form.cleaned_data['password']
			if user is not None:
				auth.login(request,user)

				ret_response = render_response(request,
							       'index.html',
							       context)
			else:
				context['message'] = "Error authenticating user"
				ret_response = render_response(request,
							       'registration/join.html',
							       context)
		else:
			context['message'] = "Error creating account."
			context['form'] = register_form
			ret_response = render_response(request,
						       'registration/join.html',
						       context)
	else:
		ret_response = render_response(request,
					       'registration/join.html',
					       context)
	return ret_response

def xmpp_auth(request):
	errors = {}
	"""auth with xmpp server."""
	username = request.POST.get('username')
	fullusername = username
	if username.find("@") == -1:
		fullusername = username + "@" + settings.XMPP_DOMAIN

	password = request.POST.get('password')
	if not request.session.test_cookie_worked():
		#set the cookie again to see if it works
		request.session.set_test_cookie()
		if not request.session.test_cookie_worked():
			errors['general'] = ['You do not seem to be accepting cookies. Please enable them and try again.']


	ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
				      request.META.get('REMOTE_ADDR',
						       '')).split(', ')[-1]
	#Validate username and password via PunJab
	try:
		pc = PunjabClient(fullusername+random_resource(),
				  password,
				  host=settings.BOSH_HOST,
				  port=settings.BOSH_PORT,
				  url=settings.BOSH_URL)
		headers =  {'Content-type': 'text/xml',
			    'X-Forwarded-For': ip_address,
			    'User-Agent': request.META.get('HTTP_USER_AGENT'),
			    'Accept': 'text/xml'}
			
		pc.startSessionAndAuth(hold='1',
				       wait='60',
				       headers = headers)
		if not pc.logged_in:
			raise NoSession
		if not pc.sid:
			raise NoSession
		ret_str = pc.sid+'_'+unicode(pc.rid)+'_'+pc.jid+'_'+pc.resource
		pcjid = pc.jid
		pcresource = pc.resource
	except (NoSession,socket.gaierror,socket.error), ex:
		errors['username'] = ['Unable to authenticate with username or password. '+str(ex)]

	return errors


def create_django_session(request):
	""" create django session."""
	username = request.POST.get('username')
	fullusername = username
	if username.find("@") == -1:
		fullusername = username + "@" + settings.XMPP_DOMAIN
	password = request.POST.get('password');
	request.session['user_password'] = password
				
	user,created = User.objects.get_or_create(username=fullusername)
	#set the given password
	user.set_password(password)
	user.save()
	user = auth.authenticate(username=user.username,
				 password=password)
	
	
	auth.login(request, user)
	

def ajax_login(request):
	"""Used to login via ajax."""
	
	username = request.POST.get('username',None)
	response_string = "<login msg=''>invalid</login>"
	valid = False
	try:
		if username:
			#errors = xmpp_auth(request)
			if not errors:
				create_django_session(request)
				valid = True
			else:
				response_string="<login msg=\""+str(errors.values()[0][0])+"\">invalid</login>"
	except Exception,ex:
		response_string = "<login msg=\"Error:"+str(ex)+"\">invalid</login>"
	if valid:
		response_string = "<login msg=''>valid</login>"
	return HttpResponse(response_string,mimetype="text/xml")
	
def login(request):
	
	redirect_to = request.REQUEST.get('next', '/')
	redirect_to = redirect_to.replace("%3A",":")
	errors = {}
	ret_response = None
	ret_str = None
	pcjid = None
	pcresource = None

	if request.method == "POST":
		
		#errors = xmpp_auth(request)
		
		#authenticate to django and update user object
		if not errors:
			try:
				create_django_session(request)
				
				ret_response = HttpResponseRedirect(redirect_to)
				
			except Exception, ex:
				errors['username'] = ['Error with username or password. ']
				ret_response = render_response(request,
							       'registration/login.html',
							       {'errors': errors,
								'next': redirect_to})				
		else:
			ret_response = render_response(request,
						       'registration/login.html',
						       {'errors': errors,
							'next': redirect_to})
	else:
		
		request.session.set_test_cookie()
		ret_response = render_response(request,
					     'registration/login.html',
					     {'errors': errors,
					      'next': redirect_to})
	return ret_response

def client(request,room_name=None,virtual_name=None):
	"""Start up the chat client with the requested room """        
	room = room_name
	if not room:
		#default room is speeqers
		room = request.GET.get('room',"speeqers")
        if virtual_name:
                room = virtual_name.replace("."+settings.HTTP_DOMAIN,"")

        userpassword = None
	pcjid = None
	pcresource = None
	fullusername = request.user.username
	ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
				      request.META.get('REMOTE_ADDR', '')).split(', ')[-1]
	if not 'nologin' in request.GET and request.user.is_authenticated(): 

		userpassword = request.session.get('user_password',None)
		
		if 'cred' in request.GET and userpassword:
			
			resp = HttpResponse(userpassword)
			resp['Expires'] = datetime.datetime.now().strftime('%a, %d %b %Y %T GMT')
			return resp
	room_theme = "client.html"
	
	return render_response(request,
			       'autologinclient.html',
			       {'username': fullusername,
				'userpassword': userpassword,
				'pcjid':pcjid,
				'pcresource':pcresource,
				'ip_address': ip_address,
				'room':room,
				'theme':'room',
				'room_theme':room_theme})


def random_resource():
	"""return random client resource """
	retval = "/spc"

	for i in range(5):
		retval += random.choice(string.letters)
	return retval

def room_message_search(request,room=None):
	"""Search rooms for chat history. """
	if not room:
		room = request.GET.get('room',None)
	user = request.GET.get('user',None)
	q = request.GET.get('q',None)
	message_type = request.GET.get('message_type',3)
	start_date = request.GET.get('start_date',None)
	end_date = request.GET.get('end_date',None)
	
	
	return render_response(request,
			       'messagesearch.html',
			       {'room':room})