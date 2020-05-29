$(document).ready(function () {

    var pathArray = window.location.pathname.split( '/' );
    var name = pathArray[pathArray.length -1];

    url = '/ajax/memberof/target/targetgroup/'
	$.get(url + name, function(data, s) {
    	if ($('#targetatargetgroup')[0] != null) {
    	$('#targetatargetgroup')[0].innerHTML=data;
        }
	});
})
