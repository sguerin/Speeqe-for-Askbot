/*
  Copyright 2010-2011 Nathan Zorn
  See LICENSE.txt

  Display the roster item.
*/
Speeqe.RosterItemView.prototype =  {
    /*
      Clones the roster item template and displays it in the roster
      item list.
    */
    show: function(roster_item,nick) {
        //if nick has our domain, erase
        nick = Strophe.unescapeNode(nick);
        var displaynick = nick.replace("@"+Speeqe.XMPP_DOMAIN,
                                       "");
        var usernamedomain = displaynick.split('@');
        var username = displaynick;
        var domainname = "";
        if(usernamedomain.length > 0)
        {
            username = usernamedomain[0];
            domainname = usernamedomain[1];
        }
        var li_clone = $("#rosteritem"+roster_item.id);
        if (li_clone.length === 0)
        {
            li_clone = $('#rosteritemtemplate').clone();
        }
        li_clone.attr("id","rosteritem"+roster_item.id);
        li_clone.attr("style","display:block");
        var online_avatar = li_clone.find("#onlineavatar");
        online_avatar.removeAttr("id");
        if (Modernizr.canvas)
        {
            var img_src = null;
            var img = false;
            if (roster_item.vcard &&
                $(roster_item.vcard).children().length > 0)
            {
                img = $(roster_item.vcard).find('BINVAL').text();
                var type = $(roster_item.vcard).find('TYPE').text();
                img_src ='data:'+ type + ';base64,'+img;
            }
            else
            {
                img_src = "/speeqe/media/images/defaultavatar.png";
            }
            if (img)
            {
                li_clone.find('.useronline').children('canvas').remove();
                li_clone.find('.useronline')
                    .prepend('<canvas id="rostercanvas'+
                             roster_item.id+
                             '" width="30" height="30"></canvas>');
                var li_canvas = li_clone.find('canvas');

                this.drawAvatar(li_canvas,
                                {src: img_src,
                                 data: img,
                                 width: 30,
                                 height: 30});
            }
            else
            {
                this.drawAvatar(online_avatar,
                                {src: img_src,
                                 data: false,
                                 width: 30,
                                 height: 30});
            }
        }
        else
        {
            online_avatar.attr("src",
                               '/speeqe/media/images/defaultavatar.png');
            online_avatar.attr("id",'onlineavatar'+roster_item.id);
            online_avatar.attr("alt",displaynick);
            online_avatar.error(function () {
                $(this).unbind("error").attr("src",
                                             "/speeqe/media/images/defaultavatar.png");
            });
        }
        li_clone.find("#roster_name").text(displaynick);
        li_clone.find("#roster_name").removeAttr("id");
        var username_elem = li_clone.find("#roster_user_name");
        if(username_elem.length > 0)
        {
            username_elem.removeAttr("id");
            username_elem.text(username);
        }
        
        var userdomain_elem = li_clone.find("#roster_user_domain");
        if(userdomain_elem.length > 0)
        {
            userdomain_elem.removeAttr("id");
            userdomain_elem.text(domainname);
        }
        
        $("#online > ul").append(li_clone.get(0));
        this.createVcard(roster_item,nick);
        this.showJoinLeave(displaynick,"joined");
    },
    //create the vcard div that is displayed on roster item mouseover.
    createVcard: function(roster_item,nick) {
        var div_clone = $('#rosteritemvcardtemplate').clone();
        if(div_clone)
        {
            div_clone.attr("id","rosteritemvcard"+roster_item.id);
            div_clone.attr("style","display:none");
            
            div_clone.css("position","absolute");
            var username_elem = div_clone.find("#vcard_name");
            if(username_elem.length > 0)
            {
                username_elem.removeAttr("id");
                username_elem.text(nick);
                div_clone.find("#vcard_name").removeAttr("id");
            }
            
            var userdomain_elem = div_clone.find("#vcard_domain");
            if(userdomain_elem.length > 0)
            {
                userdomain_elem.removeAttr("id");
                userdomain_elem.text(domainname);
            }            
            var roster_elem = $("#rosteritem"+roster_item.id);
            roster_elem.append(div_clone);
        }
    },
    
    /* Function
    Parameters:
      img_elem: the HTML element to draw the image to.
      avatar:
        avatar is an image object with src, height, width, and optional data and
        sha1 attrs.  The data attr will exist if it's HTML5 and the sha1 will
        exist if it's less than HTML5
    */
    drawAvatar: function(img_elem, avatar) {
        if (avatar.data)
        {
            var image = new Image();
            image.onload = function () {
                var ctx = img_elem.get(0).getContext('2d');                
                ctx.drawImage(image, 0, 0, avatar.width, avatar.height);
                $(img_elem.parent()).find("img").hide();
            }
            image.src = avatar.src;
        }
        else
        {
            img_elem.attr("src", avatar.src);
            img_elem.width(avatar.width + "px");
            img_elem.height(avatar.height + "px");
            if (avatar.width < 30)
            {
                img_elem.css("margin-left",
                             Math.floor((30 - avatar.width) / 2) + "px");
            }
            if (avatar.height < 30)
            {
                img_elem.css("margin-top",
                             Math.floor((30 - avatar.height) / 2) + "px");
            }
            if (Speeqe.IE6)
            {
                img_elem.attr("src","/speeqe/media/images/blank.gif");
                var filter =
                    ["progid:DXImageTransform.Microsoft.AlphaImageLoader(src='",
                     this.service,
                     "'?sha1=",
                     avatar.sha1,
                     "',sizingMethod='scale')"];
                img_elem.css("filter",filter.join(""));
            }
        }
    },
    updateVcard: function(roster_item) {
        var vcard = roster_item.vcard;
        var desc = $(vcard).find("DESC");
        var email = $(vcard).find("EMAIL");
        var url = $(vcard).find("URL");
        var roster_id = "#rosteritemvcard"+roster_item.id;        
        var roster_elem = $(roster_id);
        
        if(email.length > 0)
        {
            var email_display = jQuery.trim(email.text());
            var email_html_ar = ["email:<a href=mailto:",
                                 email_display,
                                 ">",
                                 Speeqe.urlwbr(email_display,14),
                                 "</a>"];
            roster_elem.find("#vcard_email").html(email_html_ar.join(""));
        }
        if(desc.length > 0)
        {
            var description_display = "description: " + desc.text();
            description_display =
                app.messageView().translateMessage(description_display,
                                                   false);
            roster_elem.find("#vcard_desc").html(description_display);
        }
        if(url.length > 0)
        {
            var url_html_ar = ["homepage:<a href=",
                               url.text(),
                               " target='_blank'>",
                               Speeqe.urlwbr(url.text(),14),
                               "</a>"];
            roster_elem.find("#vcard_url").html(url_html_ar.join(""));
        }
    },
    //display join room message
    showJoinLeave: function(nick,status) {
        //test if we are to display message along with chat messages.
        var chatwindow = $("#chatWindow_chatpane");        
        var cleannick = Strophe.unescapeNode(nick);
        if (chatwindow.hasClass('joinleave'))
        {
            var room_avatar = '/speeqe/media/images/murex/defaultavatar.png';
            var join_message_ar = ["<message from='",
                                   cleannick,
                                   "' to='4@dev.speeqe.com/3' id='1' type='groupchat'><x xmlns='jabber:x:event'><composing/></x><body>/me has ",
                                   status,
                                   " the room.</body></message>"];
            try {
                var join_message_jq =
                    Speeqe.text_to_xml(join_message_ar.join(""));
                app.messageView().displayMessage(nick,
                                                 room_avatar,
                                                 join_message_jq,
                                                 false);
            }
            catch(e)
            {
                console.error(e);
            }
        }
        
        var msg_template = $('#room_message_template').clone();
        msg_template.find("#nick").text(cleannick);
        $('#room_messages').append(msg_template.get(0));
    }
};
