$(document).ready(function () {
    
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Api calls
    async function apicall() {
        addurl = '/ajax/addrm/add/targetgroup/target'
        var pathArray = window.location.pathname.split( '/' );
        var targetgroupname = pathArray[pathArray.length -1];
        toadd = document.getElementById('inputaddtarget').value.split(",")
        var failed = "Error during the process for this targets: "

        // Action on items to add
        toadd.map( function(item) {
            $.ajax({
                url: addurl,
                type: 'post',
                data: {"targetname" : item, "targetgroupname": targetgroupname},
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    bootbox.alert({message:failed + item,
                                   className: "modal modal-danger fade in",
                                  })
                }
            })
        })
        // Reload
        await sleep(100)
        $('#attachedtargets').DataTable().ajax.reload(null,false);
    }


    // Add when pressing enter
    $('#inputaddtarget').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            apicall()
        }
    })


    // Add when clicking add button
    $(document).on( 'click', '#addtarget', function () {
        apicall()
    })
})
