from django.contrib.sites.models import Site
from django.template import Library, Node
import speeqeweb.xmpp.muc as muc
import speeqeweb.settings as settings

register = Library()

@register.simple_tag
def current_domain():
    return settings.HTTP_DOMAIN
@register.simple_tag
def xmpp_domain():
    return settings.XMPP_DOMAIN
    
#return all active muc rooms
class ActiveRoomsNode(Node):
    """ return all active muc rooms """

    def render(self, context):
        try:
            context['rooms'] = muc.listrooms()[:100]
        except:
            pass
        return ''
    
@register.tag(name="show_rooms")
def show_rooms(parser,token):
    return ActiveRoomsNode()

class DnsRoomNamesNode(Node):
    """ return setting that the dns trick for room names is being used """
    def render(self, context):
        try:
            context['dns_room_names'] = settings.DNS_ROOM_NAMES
        except:
            pass
        return ''
    
@register.tag(name="use_dns_room_names")
def use_dns_room_names(parser,token):
    return DnsRoomNamesNode()

