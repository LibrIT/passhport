$(document).ready(function () {

    //to handle the targetgroup name (used in attachedtargets datatable)
    var pathArray = window.location.pathname.split( '/' );
    var targetgroupname = pathArray[pathArray.length -1];
    var attachedtargeturl = "/ajax/attached/targetgroup/targets/";
	

    //Datatables definitions
    $('#attachedtargets').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        "language": {
            "emptyTable": "No target is attached to this targetgroup"
        },
        columnDefs: [ {
            targets: "nosort",
            "orderable": false,
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : attachedtargeturl.concat(targetgroupname),
            dataSrc : 'data'
        }
    })    

    // Ask to validate before removing target from targetgroup
    $('#attachedtargets tbody').on( 'click', '#deleteclose', function () {
        span = $(this).children("#butdelspan")[0];
        namecell = $(this).parents('tr').children('td')[0]
        lastlogcell = $(this).parents('tr').children('td')[1]
        name = namecell.innerText.replace(/\n/g, '')
        button = this

        // First click
        if (span.innerText != "Undo") {
            //Delete target from targetgroup in ajax
            $.ajax({
                url: '/ajax/addrm/rm/targetgroup/target',
                type: 'post',
                data: {targetname : name, targetgroupname: targetgroupname},
                //{targetname : String(name), targetgroupname : String(targetgroupname)},
                success: function() {
                    // Graphical hints
                    span.innerText = "Undo"
                    button.className = "deleteundo"
                    namecell.classList.add("table-cell-removed")
                    lastlogcell.classList.add("table-cell-removed")
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error removing this target. Is passhportd still up?")
                }
            });

        } else {
            //Add the target to the targetgroup
            $.ajax({
                url: '/ajax/addrm/add/targetgroup/target',
                type: 'post',
                data: {targetname : name, targetgroupname : targetgroupname},
                success: function() {
                    // Graphical hints
                    span.innerText = "\xD7"
                    button.className = "deleteclose"
                    namecell.classList.remove("table-cell-removed")
                    lastlogcell.classList.remove("table-cell-removed")
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    alert("Error adding this target. Is passhportd still up?")
                }
            });
        }
    } )
})
