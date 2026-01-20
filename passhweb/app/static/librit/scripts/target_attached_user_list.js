$(document).ready(function () {

    //to handle the target name (used in attachedusers datatable)
    var pathArray = window.location.pathname.split( '/' );
    var targetname = pathArray[pathArray.length -1];
    var attacheduserurl = "/ajax/attached/target/users/";

    //Datatables definitions
    $('#attachedusers').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        "language": {
            "emptyTable": "No user is attached to this target"
        },
        columnDefs: [ {
            targets: "nosort",
            "orderable": false,
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : attacheduserurl.concat(targetname),
            dataSrc : 'data'
        }
    })    

    // Ask to validate before removing user from target
    $('#attachedusers tbody').on( 'click', '#deleteclose', function () {
        span = $(this).children("#butdelspan")[0];
        namecell = $(this).parents('tr').children('td')[0]
        lastlogcell = $(this).parents('tr').children('td')[1]
        name = namecell.innerText.replace(/\n/g, '')
        button = this

        // First click
        if (span.innerText != "Undo") {
            //Delete user from target in ajax
            $.ajax({
                url: '/ajax/addrm/rm/target/user',
                type: 'post',
                data: {username : name, targetname: targetname},
                //{username : String(name), targetname : String(targetname)},
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
            //Add the user to the target
            $.ajax({
                url: '/ajax/addrm/add/target/user',
                type: 'post',
                data: {username : name, targetname : targetname},
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
