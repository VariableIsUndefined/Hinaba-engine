var style_cookie;

function getCookie(name) {
	with(document.cookie) {
		var regexp=new RegExp("(^|;\\s+)"+name+"=(.*?)(;|$)");
		var hit=regexp.exec(document.cookie);
		if(hit&&hit.length>2) return Utf8.decode(unescape(replaceAll(hit[2],'+','%20')));
		else return '';
	}
}

function set_cookie(name,value,days) {
	if(days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires="; expires="+date.toGMTString();
	} else expires="";

	document.cookie = name + "=" + value + expires+"; path=/";
}

function set_stylesheet(style_title) {
	set_cookie(style_cookie, style_title, 365);

	var links = document.getElementsByTagName("link");
	var found = false;

	for(var i=0; i < links.length; i++) {
		var rel=links[i].getAttribute("rel");
		var title=links[i].getAttribute("title");
		
		if(rel.indexOf("style") != -1 && title) {
			links[i].disabled=true; // IE needs this to work. IE needs to die.
			if(style_title == title) {
                 links[i].disabled=false;
                 found=true; 
            }
		}
	}
	if(!found) set_preferred_stylesheet();
}

function set_preferred_stylesheet() {
	var links = document.getElementsByTagName("link");
	for(var i=0; i < links.length; i++) {
		var rel=links[i].getAttribute("rel");
		var title=links[i].getAttribute("title");
		if(rel.indexOf("style")!=-1&&title) links[i].disabled = (rel.indexOf("alt") != -1);
	}
}

function get_active_stylesheet() {
	var links = document.getElementsByTagName("link");
	for(var i=0; i < links.length; i++) {
		var rel=links[i].getAttribute("rel");
		var title=links[i].getAttribute("title");
		if(rel.indexOf("style") != -1 && title && !links[i].disabled) return title;
	}
	
	return null;
}

function get_preferred_stylesheet() {
	var links = document.getElementsByTagName("link");
	for(var i=0; i<links.length; i++) {
		var rel=links[i].getAttribute("rel");
		var title=links[i].getAttribute("title");
		if(rel.indexOf("style")!=-1 && rel.indexOf("alt")==-1&&title) return title;
	}
	
	return null;
}

window.onbeforeunload = function() {
	if(style_cookie) {
		var title = get_active_stylesheet();
		set_cookie(style_cookie,title,365);
	}
}

if(style_cookie) {
	var cookie = getCookie(style_cookie);
	var title = cookie ? cookie : get_preferred_stylesheet();

	set_stylesheet(title);
}