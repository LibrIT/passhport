$(document).ready(function () {

    //to handle the target name (used in attachedusers datatable)
    var pathArray = window.location.pathname.split( '/' );
    var targetgroupname = pathArray[pathArray.length -1];
    var attachedusergroupurl = "/ajax/attached/targetgroup/usergroups/";

    //Datatables definitions
    $('#attachedusergroups').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        'deferRender' : true,
        "language": {
            "emptyTable": "No usergroup is attached to this targetgroup"
        },
        columnDefs: [ {
            targets: "nosort",
            "orderable": false,
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : attachedusergroupurl.concat(targetgroupname),
            dataSrc : 'data'
        }
    })    

    // Ask to validate before removing usergroup from target
    $('#attachedusergroups tbody').on( 'click', '#deleteclose', function () {
        span = $(this).children("#butdelspan")[0];
        namecell = $(this).parents('tr').children('td')[0]
        lastlogcell = $(this).parents('tr').children('td')[1]
        name = namecell.innerText.replace(/\n/g, '')
        button = this

        // First click
        if (span.innerText != "Undo") {
            //Delete user from target in ajax
            $.ajax({
                url: '/ajax/addrm/rm/targetgroup/usergroup',
                type: 'post',
                data: {usergroupname : name, targetgroupname: targetgroupname},
                success: function() {
                    // Graphical hints
                    span.innerText = "Undo"
                    button.className = "deleteundo"
                    namecell.classList.add("table-cell-removed")
                    lastlogcell.classList.add("table-cell-removed")
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error removing this usergroup. Is passhportd still up?")
                }
            });

        } else {
            //Add the user to the target
            $.ajax({
                url: '/ajax/addrm/add/targetgroup/usergroup',
                type: 'post',
                data: {usergroupname : name, targetgroupname : targetgroupname},
                success: function() {
                    // Graphical hints
                    span.innerText = "\xD7"
                    button.className = "deleteclose"
                    namecell.classList.remove("table-cell-removed")
                    lastlogcell.classList.remove("table-cell-removed")
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error adding this usergroup. Is passhportd still up?")
                }
            });
        }
    } )
})
