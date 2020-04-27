$(document).ready(function () {
    // Api calls
    function apicall() {
        addurl = '/ajax/addrm/add/usergroup/user'
        var pathArray = window.location.pathname.split( '/' );
        var usergroupname = pathArray[pathArray.length -1];
        toadd = document.getElementById('inputadduser').value.split(",")
        var failed = "Error during the process for this users: "

        // Action on items to add
        toadd.map( function(item) {
            $.ajax({
                url: addurl,
                type: 'post',
                data: {"username" : item, "usergroupname": usergroupname},
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    bootbox.alert({message:failed + item,
                                   className: "modal modal-danger fade in",
                                  })
                }
            })
        })
        // Sometimes needs to be reloaded twice... dirty but works
        $('#attachedusers').DataTable().ajax.reload();
        $('#inputadduser').val('');
        $('#attachedusers').DataTable().ajax.reload();
    }


    // Add when pressing enter
    $('#inputadduser').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            apicall()
        }
    })


    // Add when clicking add button
    $(document).on( 'click', '#adduser', function () {
        apicall()
    })
})
