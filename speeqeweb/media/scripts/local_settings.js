//domain for your website (used to build url in java scripts)
Speeqe.HTTP_DOMAIN = "tribe";
//domain for your jabber server
Speeqe.XMPP_DOMAIN = "tribe";
//domain for your multi user chat server
//multi user chat server name. This is the default chat server used if
//none is provided. If you connect to a room, the room will be
//room@Speeqe.CHAT_SERVER.
Speeqe.CHAT_SERVER = "conference.tribe.fr.murex.com";
//allows users to use the /nick command to change their muc name
Speeqe.ENABLE_NICK_CHANGE = false;
//the default chat room if none is specified. If a muc room is not
//provided, and the user connects, this will be the default room.
Speeqe.DEFAULT_CHAT_ROOM = "default@conference.tribe.com";

//the url used to proxy to your BOSH server.  Used by speeqe to
//communicate with the bosh server.
Speeqe.BOSH_URL =  "/http-bind";

//This is used to add additional help information to the help
//dialog. It will be displayed right before the instructions to close
//the dialog.
Speeqe.helpDialogHtml = "";

/* 

use this function to replace the anonymous nick selection. The default
function picks from a list of president names ,Speeqe.NAMES. See
anonymous.js for more details.

*/
/* list of anonymous nicks
Speeqe.NAMES = ["anonymous"];
Speeqe.generate_anonymous_nick = function() {

};
*/
