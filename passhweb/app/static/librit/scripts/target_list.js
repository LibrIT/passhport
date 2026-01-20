$(document).ready(function () {
    $('#targetslist').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        'deferRender' : true,
        'ajax'        : {
            url     : '/ajax/list/targets',
            dataSrc : 'data'
        }
    })
})
    
