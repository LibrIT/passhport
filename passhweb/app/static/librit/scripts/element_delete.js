$(document).ready(function () {
    // Api calls
    function apicall() {
        var pathArray = window.location.pathname.split( '/' );
        var eltname = pathArray[pathArray.length -1];
        var elttype = pathArray[pathArray.length -2];
        url = '/ajax/delete/' + elttype;
       
        $.get(url + "/" + eltname, function() {
            window.location.href = '/list/' + elttype;
        });
    };

    // react when clicking delete button
    $(document).on( 'click', '#delete', function () {
        bootbox.confirm({message: "Are you sure to definitively delete this element?", 
                         className: "modal modal-danger fade in",
                         callback: function(answer) {
                            if (answer) {
                                apicall()
                            }
                        }});
    });
})
