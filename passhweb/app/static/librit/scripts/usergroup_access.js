$(document).ready(function () {

    var pathArray = window.location.pathname.split( '/' );
    var usergroupname = pathArray[pathArray.length -1];

    url = '/ajax/access/usergroup/'
	$.get(url + usergroupname, function(data, s) {
    	$('#usergroupaccess')[0].innerHTML=data;
	});
    url = '/ajax/memberof/usergroup/target/'
	$.get(url + usergroupname, function(data, s) {
    	$('#usergroupatarget')[0].innerHTML=data;
	});
    url = '/ajax/memberof/usergroup/targetgroup/'
	$.get(url + usergroupname, function(data, s) {
    	$('#usergroupatargetgroup')[0].innerHTML=data;
	});
    url = '/ajax/memberof/usergroup/usergroup/'
	$.get(url + usergroupname, function(data, s) {
    	$('#usergroupausergroup')[0].innerHTML=data;
	});
})
