$(document).ready(function () {

    //to handle the usergroup name (used in attachedusers datatable)
    var pathArray = window.location.pathname.split( '/' );
    var usergroupname = pathArray[pathArray.length -1];
    var attacheduserurl = "/ajax/attached/usergroup/users/";

    //Datatables definitions
    $('#attachedusers').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        "language": {
            "emptyTable": "No user is attached to this usergroup"
        },
        columnDefs: [ {
            targets: "nosort",
            "orderable": false,
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : attacheduserurl.concat(usergroupname),
            dataSrc : 'data'
        }
    })    

    // Ask to validate before removing user from usergroup
    $('#attachedusers tbody').on( 'click', '#deleteclose', function () {
        span = $(this).children("#butdelspan")[0];
        namecell = $(this).parents('tr').children('td')[0]
        lastlogcell = $(this).parents('tr').children('td')[1]
        name = namecell.innerText.replace(/\n/g, '')
        button = this

        // First click
        if (span.innerText != "Undo") {
            //Delete user from usergroup in ajax
            $.ajax({
                url: '/ajax/addrm/rm/usergroup/user',
                type: 'post',
                data: {username : name, usergroupname: usergroupname},
                //{username : String(name), usergroupname : String(usergroupname)},
                success: function() {
                    // Graphical hints
                    span.innerText = "Undo"
                    button.className = "deleteundo"
                    namecell.classList.add("table-cell-removed")
                    lastlogcell.classList.add("table-cell-removed")
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error removing this user. Is passhportd still up?")
                }
            });

        } else {
            //Add the user to the usergroup
            $.ajax({
                url: '/ajax/addrm/add/usergroup/user',
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
                    alert("Error adding this user. Is passhportd still up?")
                }
            });
        }
    } )
})
