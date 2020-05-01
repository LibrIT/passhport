$(document).ready(function () {

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Api calls
    async function apicall() {
        addurl = '/ajax/addrm/add/usergroup/manager'
        var pathArray = window.location.pathname.split( '/' );
        var usergroupname = pathArray[pathArray.length -1];
        toadd = document.getElementById('inputaddmanager').value.split(",")
        var failed = "Error during the process for this manager: "

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
        await sleep(100)
        $('#inputadduser').val('');
        $('#attachedmanager').DataTable().ajax.reload();
    }


    // Add when pressing enter
    $('#inputaddmanager').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            apicall()
        }
    })


    // Add when clicking add button
    $(document).on( 'click', '#addmanager', function () {
        apicall()
    })
})
