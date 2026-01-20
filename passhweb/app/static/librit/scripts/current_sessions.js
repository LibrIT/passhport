$(document).ready(function () {

    var url = "/ajax/connection/ssh/current";

    //Datatables definitions
    $('#sshsessions').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        "language": {
            "emptyTable": "No one is connected via PaSSHport..."
        },
        columnDefs: [ {
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : url,
            dataSrc : 'data'
        }
    })    

    // Disconnection button
    $('#sshsessions tbody').on( 'click', '#deleteclose', function () {
        span = $(this).children("#butdelspan")[0];
        namecell = $(this).parents('tr').children('td')[3]
        name = namecell.innerText.replace(/\n/g, '')
        button = this

	    $.get("/ajax/connection/ssh/disconnect/" + name, function(data, s) {
            $('#sshsessions').DataTable().ajax.reload();
	    });
    } )

    //Datatables definitions
    $('#dbsessions').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        "language": {
            "emptyTable": "No one is connected via PaSSHport..."
        },
        columnDefs: [ {
            targets: "nosort",
            "orderable": false,
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : '/ajax/connection/db/current',
            dataSrc : 'data'
        }
    })    
    // Disconnection button
    $('#dbsessions tbody').on( 'click', '#accessclose', function () {
        span = $(this).children("#butdelspan")[0];
        namecell = $(this).parents('tr').children('td')[2]
        targetname = namecell.innerText.replace(/\n/g, '')
        namecell = $(this).parents('tr').children('td')[1]
        username = namecell.innerText.replace(/\n/g, '')
        button = this

	    $.get("/ajax/user/database/access/close/" + targetname +  "/" + username, function(data, s) {
            $('#dbsessions').DataTable().ajax.reload();
	    });
    } )



})
