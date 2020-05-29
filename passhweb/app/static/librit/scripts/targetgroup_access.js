$(document).ready(function () {

    var pathArray = window.location.pathname.split( '/' );
    var usergroupname = pathArray[pathArray.length -1];

    url = '/ajax/access/targetgroup/'
	$.get(url + usergroupname, function(data, s) {
    	$('#targetgroupaccess')[0].innerHTML=data;
	});
    url = '/ajax/memberof/targetgroup/targetgroup/'
	$.get(url + usergroupname, function(data, s) {
    	$('#targetgroupatargetgroup')[0].innerHTML=data;
	});
})
