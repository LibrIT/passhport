$(document).ready(function () {

    var pathArray = window.location.pathname.split( '/' );
    var username = pathArray[pathArray.length -1];

    url = '/ajax/access/user/'
	$.get(url + username, function(data, s) {
    	$('#useraccess')[0].innerHTML=data;
	});
    url = '/ajax/memberof/user/target/'
	$.get(url + username, function(data, s) {
    	$('#useratarget')[0].innerHTML=data;
	});
    url = '/ajax/memberof/user/targetgroup/'
	$.get(url + username, function(data, s) {
    	$('#useratargetgroup')[0].innerHTML=data;
	});
    url = '/ajax/memberof/user/usergroup/'
	$.get(url + username, function(data, s) {
    	$('#userausergroup')[0].innerHTML=data;
	});
})
