
#
# Copyright (c) 2005 - 2008 Nathan Zorn, OGG, LLC 
# See LICENSE.txt for details
#

import xmpp
import speeqeweb.settings


class XMMPAuthError(Exception):
    """Unable to authenticate to configured xmpp server. """
    def __str__(self):
        return "Unable to authenticate to xmpp server."

class XMMPConnectError(Exception):
    """Unable to connect to xmpp server. """
    def __str__(self):
        return "Unable to connect to xmpp server."

class ChatRoom:		
    def __init__(self, name, description, occupants, creationdate):
        self.name = name
        self.description = description
        self.occupants = occupants
        self.creationdate = creationdate

class RoomQuery:
    def __init__(self):
        self.name = []
        self._ns = 'http://jabber.org/protocol/disco#items'
        
    def xmpp_result(self,func,response):    
        """Used to retrieve the list of rooms from the conference service. """

        if response.getType() == 'result':
            for node in response.getQueryPayload():
                room_jid = node.getAttr('jid')
                #room_name = room_jid.split('@')[0]
                room_name = node.getAttr('name')
                #self.rooms.append(room_name)
                # query details of each room
                jid=xmpp.protocol.JID(node=speeqeweb.settings.XMPP_USER,domain=speeqeweb.settings.XMPP_DOMAIN,resource='/listrooms')
                client = xmpp.Client(jid.getDomain(),debug=[])
                if client.connect(use_srv=True):
                    if client.auth(jid.getNode(),speeqeweb.settings.XMPP_PASS,sasl=1):
                        self._ns = 'http://jabber.org/protocol/disco#info'
                        iq = xmpp.protocol.Iq(typ='get',
                                              to=room_jid,)
                        query = iq.setTag("query",namespace=self._ns)
                        responsedetail = client.SendAndWaitForResponse(iq)						
                        if responsedetail.getType() == 'result':
                            for node_x in responsedetail.getQueryPayload():
                                if node_x.getName() == 'x':
                                    for node_field in node_x.getPayload():
                                        if node_field.getAttr('var') == 'muc#roominfo_description':
                                            for node_value in node_field.getPayload():
                                                room_desc = node_value.getData()
                                        if node_field.getAttr('var') == 'muc#roominfo_occupants':
                                            for node_value in node_field.getPayload():
                                                room_occupants = node_value.getData()
                                        if node_field.getAttr('var') == 'x-muc#roominfo_creationdate':
                                            for node_value in node_field.getPayload():
                                                room_creationdate = node_value.getData()
                                                room_creationday,room_creationhour = room_creationdate.split("T")
                                                room_creationdate = room_creationday + ' ' + room_creationhour
						client.disconnect()
						room = ChatRoom(name = room_name,
                                        description = room_desc,
                                        occupants = room_occupants,
                                        creationdate = room_creationdate)
                        self.rooms.append(room)
                    else:
                        print "Unable to authenticate via xmpp."
                else:
                    print "Unable to connect via xmpp."

    def queryRooms(self):
        #jid=xmpp.protocol.JID(speeqeweb.settings.XMPP_USER+"/listrooms")
        jid=xmpp.protocol.JID(node=speeqeweb.settings.XMPP_USER,domain=speeqeweb.settings.XMPP_DOMAIN,resource='/listrooms')
        client = xmpp.Client(jid.getDomain(),debug=[])
        if client.connect(use_srv=True):
            if client.auth(jid.getNode(),speeqeweb.settings.XMPP_PASS,sasl=1):
                iq = xmpp.protocol.Iq(typ='get',
                                      to=speeqeweb.settings.XMPP_CHAT,)
                query = iq.setTag("query",namespace=self._ns)            
                
                response = client.SendAndWaitForResponse(iq)
                self.xmpp_result(self.xmpp_result,response)
                
                client.disconnect()
            else:
                print "Unable to authenticate via xmpp."

        else:
            print "Unable to connect via xmpp."

def listrooms():
    """Return rooms in chat service for configured chat server."""
    room_query = RoomQuery()
    retval = []
    try:
        room_query.queryRooms()
        retval = room_query.rooms        
    except Exception, ex:
        print str(ex)
    return retval

if __name__ == '__main__':
    print listrooms()
