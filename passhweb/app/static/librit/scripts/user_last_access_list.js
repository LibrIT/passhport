$(document).ready(function () {
    var pathArray = window.location.pathname.split( '/' );
    var username = pathArray[pathArray.length -1];

    $('#targetsaccesslist').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        'deferRender' : true,
        "language": {
            "emptyTable": "This user seems to have no access..."
        },
        'ajax'        : {
            url     : '/ajax/list/accesstargets/' + username,
            dataSrc : 'data'
        }
    })
})
    
