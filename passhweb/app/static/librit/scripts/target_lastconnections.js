$(document).ready(function () {
    var pathArray = window.location.pathname.split( '/' );
    var targetname = pathArray[pathArray.length -1];
    
    $('#targetloglist').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'order'       : [[0, "desc"]],
        'info'        : true,
        'autoWidth'   : true,
        'deferRender' : true,
        "language": {
            "emptyTable": "No connection history for this target"
        },
        'ajax'        : {
            url     : '/ajax/target/lastconnections/' + targetname,
            dataSrc : 'data'
        }
    })
})
    
