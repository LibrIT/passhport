$(document).ready(function () {

    function sleep(ms) {
          return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Api calls
    async function apicall() {
        addurl = '/ajax/addrm/add/target/usergroup'
        //to handle the usergroup name (used in attachedusers datatable)
        var pathArray = window.location.pathname.split( '/' );
        var name = pathArray[pathArray.length -1];
        toadd = document.getElementById('inputaddusergroup').value.split(",")
        var failed = "Error during the process for this usergroup: "

        // Action on items to add
        toadd.map( function(item) {
            $.ajax({
                url: addurl,
                type: 'post',
                data: {"usergroupname" : item, "targetname": name},
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    bootbox.alert({message: failed + item,
                                   className: "modal modal-danger fade in",
                                  })
                }
            })
        })
        // Reload datatable
		await sleep(100)
        $('#attachedusergroups').DataTable().ajax.reload(null, false);
    }


    // Add when pressing enter
    $('#inputaddusergroup').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            apicall()
        }
    })


    // Add usergroup when clicking add button
    $(document).on( 'click', '#addusergroup', function () {
        apicall()
    })
})

