$(document).ready(function () {

    //to handle the usergroup name (used in attachedusers datatable)
    var pathArray = window.location.pathname.split( '/' );
    var usergroupname = pathArray[pathArray.length -1];
    var url = "/ajax/attached/usergroup/manager/";

    //Datatables definitions
    $('#attachedmanager').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        "language": {
            "emptyTable": "No manager is attached to this usergroup"
        },
        columnDefs: [ {
            targets: "nosort",
            "orderable": false,
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : url.concat(usergroupname),
            dataSrc : 'data'
        }
    })    

    // Ask to validate before removing user from usergroup
    $('#attachedmanager tbody').on( 'click', '#deleteclose', function () {
        span = $(this).children("#butdelspan")[0];
        namecell = $(this).parents('tr').children('td')[0]
        lastlogcell = $(this).parents('tr').children('td')[1]
        name = namecell.innerText.replace(/\n/g, '')
        button = this

        // First click
        if (span.innerText != "Undo") {
            //Delete user from usergroup in ajax
            $.ajax({
                url: '/ajax/addrm/rm/usergroup/manager',
                type: 'post',
                data: {username : name, usergroupname: usergroupname},
                success: function() {
                    // Graphical hints
                    span.innerText = "Undo"
                    button.className = "deleteundo"
                    namecell.classList.add("table-cell-removed")
                    lastlogcell.classList.add("table-cell-removed")
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error removing this manager. Is passhportd still up?")
                }
            });

        } else {
            //Add the user to the usergroup
            $.ajax({
                url: '/ajax/addrm/add/usergroup/manager',
                type: 'post',
                data: {username : name, usergroupname : usergroupname},
                success: function() {
                    // Graphical hints
                    span.innerText = "\xD7"
                    button.className = "deleteclose"
                    namecell.classList.remove("table-cell-removed")
                    lastlogcell.classList.remove("table-cell-removed")
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error adding this manager. Is passhportd still up?")
                }
            });
        }
    } )
})
