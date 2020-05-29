$(document).ready(function () {
    
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Api calls
    async function apicall() {
        addurl = '/ajax/addrm/add/targetgroup/targetgroup'
        var pathArray = window.location.pathname.split( '/' );
        var targetgroupname = pathArray[pathArray.length -1];
        toadd = document.getElementById('inputaddtargetgroup').value.split(",")
        var failed = "Error during the process for this targetgroup: "

        // Action on items to add
        toadd.map( function(item) {
            $.ajax({
                url: addurl,
                type: 'post',
                data: {"subtargetgroupname" : item, "targetgroupname": targetgroupname},
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    bootbox.alert({message:failed + item,
                                   className: "modal modal-danger fade in",
                                  })
                }
            })
        })
        // reload
        await sleep(100)
        $('#attachedtargetgroups').DataTable().ajax.reload(null,false);
    }


    // Add when pressing enter
    $('#inputaddtargetgroup').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            apicall()
        }
    })


    // Add when clicking add button
    $(document).on( 'click', '#addtargetgroup', function () {
        apicall()
    })
})
