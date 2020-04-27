$(document).ready(function () {
    // Api calls
    function apicall() {
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
        // Sometimes needs to be reloaded twice... dirty but works
        $('#attachedtargetgroups').DataTable().ajax.reload();
        $('#inputaddtargetgroup').val('');
        $('#attachedtargetgroups').DataTable().ajax.reload();
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
