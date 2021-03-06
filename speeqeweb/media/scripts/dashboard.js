/*

Copyright 2007-2008 OGG, LLC
See LICENSE.txt

  Inserts the speeqe dashboard into the interface.  Also includes the
  UI and code to make the dashboard work.

*/


Speeqe.dashBoardInit = function() {

    
    //dashboard html
    var dashboard_html = "<div id=\"dashboard\"> \
                        <div class=\"control item\"> \
                            <span id=\"roomname\"></span>@<span id=\"roomdomainname\"></span> \
                        </div> \
                        <div id=\"free-space\" class=\"item\"> \
                                <p></p> \
                        </div> \
                        <div id=\"right-control\" class=\"control item\"> \
                                <ul> \
                                        <li class=\"button\"> \
                                                <p id='show_help_dialog' class=\"menu-item\"><span>Help</span></p> \
                                        </li> \
                                        <li class=\"button\"> \
                                                <p id='configure_chat' class=\"menu-item\"><span>Settings</span></p> \
                                        </li> \
                                </ul> \
                        </div> \
                </div> \
";
    var dashboard_elem = $(dashboard_html);
    var style_elem = "<link rel=\"stylesheet\" type=\"text/css\" href=\"/speeqe/media/css/dashboard.css\" />";
    $("head").append(style_elem);
    //test if ie and add ie specific style
    if($.browser.msie)
    {
	var style_elem_ie = "<link rel=\"stylesheet\" type=\"text/css\" href=\"/speeqe/media/css/dashboardie.css\" />";
	$("head").append(style_elem_ie);
    }
    $("body").prepend(dashboard_elem);
    
    $("#dashboard ul li ul").css("top",30);
    $("#right-control ul li ul").css("left",-($("#settings span").width() + 9));
    $(document).bind('mousedown', Speeqe.dashboardMouseCheck);
};


Speeqe.dashboardMouseCheck = function(e) {

    $("#dashboard ul li ul").each( function (i,elem) {

	if($(elem).css("display") != "none")
	{
	    //only hide menu if clicked outside of control
	    if($(e.target).parents(".control").length == 0)
	    {
		$(elem).parent("li").click();
	    }

	}
    });

};
