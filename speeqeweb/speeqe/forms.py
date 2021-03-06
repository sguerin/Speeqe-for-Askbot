#
# Copyright (c) 2005 - 2008 Nathan Zorn, OGG, LLC 
# See LICENSE.txt for details
#


from django import forms
from speeqeweb.settings import HTTP_DOMAIN,XMPP_DOMAIN,EXACT_BAD_WORDS,MATCH_BAD_WORDS
from django.conf import settings
from django.contrib.auth.models import User
import datetime

#error strings used when throwing form validation exceptions. An
#exception class might be overkill?
error_strings = {
    'existing':'There is already an account under this username.',
    'existing_email':"There is already an account under this email address. If you forgot your user information, go <a href='/forgot/'> here</a>.",
    'invalid_domain':"You can not use a %s email address. Please try again.",
    'invalid_email':"That email address isn't valid, please try again.",
    'invalid_characters':"Invalid characters in username.",
    }

#Used to register users for speeqe
class RegisterForm(forms.Form):
    email = forms.EmailField(label="Email",
                             max_length=75,
                             widget=forms.TextInput(attrs={'size': 25}))
    username = forms.CharField(label="Username",
                               widget=forms.TextInput(attrs={'size': 25}))
    
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(attrs={'size': 25}),
                               min_length=6,
                               max_length=30)

    def save(self):
        username,realm = self.cleaned_data['username'].split("@")
        username = self.cleaned_data['username'].strip()
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        try:
            new_user = None

            try:
                new_user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass

            if not new_user:
                new_user = User.objects.create_user(username,
                                 email,
                                 username)
                new_user.save()

            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.last_login = datetime.datetime.utcnow()		
            new_user.save()
        except Exception, ex:
            raise forms.ValidationError(error_strings['existing']+str(ex))

        return new_user
    
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        return validate_email(email)

    def clean_username(self):
        """Validates username"""
        username = self.cleaned_data['username'].strip()
        return validate_username(username)

def validate_email(email):
    try:
        existing = User.objects.get(email=email)
        if existing is not None:
            raise forms.ValidationError(error_strings['existing_email'])
            
    except User.DoesNotExist:
        pass

    if email.find(HTTP_DOMAIN) != -1:
        raise forms.ValidationError(error_strings['invalid_domain']%HTTP_DOMAIN)


#    try:
#        domainname = email.split("@")[1]
#        import dns.resolver
#        answers = dns.resolver.query(domainname.encode('utf8'), 'MX')
#    except ImportError:
#        pass
#    except:
#        raise forms.ValidationError(error_strings['invalid_email'])


    tuser, thost = email.split('@', 1)
    if tuser in EXACT_BAD_WORDS:
        raise forms.ValidationError(error_strings['invalid_characters'])
        
    for wrd in MATCH_BAD_WORDS:
        if email.find(wrd) != -1:
            raise forms.ValidationError(error_strings['invalid_characters'])
            
    if email.count('@') > 1:
        raise forms.ValidationError(error_strings['invalid_characters'])
        

    return email

#leave this as the last function for emacs sake. the disallowed
#string doesn't play nice
def validate_username(username):
    if username.count(" ") > 1:
        raise forms.ValidationError("Spaces are not allowed in usernames.")


    if User.objects.filter(username__iexact=username).count() > 0:
        raise forms.ValidationError("Username is already in use.")

    if username.count("@") > 0:
        raise forms.ValidationError("Usernames can not have more than one @ in them.")

    if username.count("@") == 0:
        username += "@" + XMPP_DOMAIN
    
    # check for invalid characters
    disallowed = """&"'/:<>\\"""

    for c in disallowed:
        if c in username:
            raise forms.ValidationError("Usernames cannot contain the following character: "+c)

    
    return username
