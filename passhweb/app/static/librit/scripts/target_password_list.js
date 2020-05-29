$(document).ready(function () {

    //to handle the target name
    var pathArray = window.location.pathname.split( '/' );
    var targetname = pathArray[pathArray.length -1];
    var url = "/ajax/target/password/";

    //Datatables definitions
    $('#targetpassword').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'order': [[0, "desc"]],
        'info'        : true,
        'autoWidth'   : true,
        "language": {
            "emptyTable": "No password associated to this target"
        },
        columnDefs: [ {
            targets: "nosort",
            "orderable": false,
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : url.concat(targetname),
            dataSrc : 'data'
        }
    })    
})
