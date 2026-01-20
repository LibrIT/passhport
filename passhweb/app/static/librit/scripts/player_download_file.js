$(document).ready(function () {
    // Api calls
    function apicall() {
        var url        = '/download'
        var prepurl    = '/ajax/prepdownload'
        var pathArray  = window.location.pathname.split( '/' );
        var targetname = pathArray[pathArray.length -1];
        var filename   = document.getElementById('inputdownload').value
        var playername = document.getElementById('inputplayer').value
        var failed     = "Error during the process for this file: </br> - Check the file path</br>- Support only one file at a time</br> - The target login must have the right on the file</br>- Special system files will be empty (eg: /proc/cpuinfo)"

        // Check if file can be downloaded
        $.ajax({
            url: prepurl,
                type: 'post',
                data: {"targetname" : targetname, "filename": filename, "player": playername},
                success: function(data){
                    jQuery.download(url, targetname, filename, playername)
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    bootbox.alert({message:failed,
                                   className: "modal modal-danger fade in",
                                  })
                },
        })
	}

	jQuery.download = function(url, targetname, filename, playername, go){
            // Build a form
            var form = $('<form></form>').attr('action', url).attr('method', 'POST')
            // Add the one key/values
            form.append($("<input></input>").attr('type', 'hidden').attr('name', "targetname").attr('value', targetname));
            form.append($("<input></input>").attr('type', 'hidden').attr('name', "player").attr('value', playername));
            form.append($("<input></input>").attr('type', 'hidden').attr('name', "filename").attr('value', filename));
            //send request
            form.appendTo('body').submit().remove();
	};
    


    // Add when pressing enter
    $('#inputdownload').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            apicall()
        }
    })

    // Add when pressing enter
    $('#inputplayer').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            apicall()
        }
    })



    // Add when clicking add button
    $(document).on( 'click', '#downloadfile', function () {
        apicall()
    })
})
