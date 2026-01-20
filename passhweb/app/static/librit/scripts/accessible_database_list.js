$(document).ready(function () {
    $('#targetslist').DataTable({
        'paging'      : true,
        'lengthChange': false,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'autoWidth'   : true,
        'deferRender' : true,
        "language": {
            "emptyTable": "Currently you haven't any databases access rights. You can contact a passhport administrator if you think that is a mistake."
        },
        columnDefs: [ {
            targets: "nosort",
            "orderable": false,
            "width"    : "33px"
        } ],
        'ajax'        : {
            url     : '/ajax/user/database/list',
            dataSrc : 'data'
        }
    })

    // Pushing close button to close the connection
    $('tbody').on( 'click', '#accessclose', function () {
        closebutton = this
        firstcell = $(this).parents('tr').children('td')[0]
        openbutton = $(this).parents('tr').children('td')[3].children[0]
        target = firstcell.innerText
            
        $.ajax({
            url: '/ajax/user/database/access/close/' + target,
            type: 'get',
            success: function(data) {
                openbutton.innerText = data
                openbutton.classList.add("btn-primary")
                openbutton.classList.add("btn")
                openbutton.classList.remove("btn-success")
                openbutton.classList.remove("btn-danger")
                closebutton.style.visibility = 'hidden'
            }
        });
    })


    // Pushing the askbutton open a connexion for user IP
    $('tbody').on( 'click', '#accessask', function () {
        button = this
        closebutton = $(this).parents('tr').children('td')[4].children[0]
        firstcell = $(this).parents('tr').children('td')[0]
        lastcell = $(this).parents('tr').children('td')[4]
        target = firstcell.innerText

        // First time we press the button, we open a connection
        if(button.classList.contains("btn-primary")) {
            $.ajax({
                url: '/ajax/user/database/access/' + target,
                type: 'get',
                success: function(data) {
                    button.innerText = data
		            if(data.includes("ERROR")) {
                        button.classList.add("btn-danger")
                        button.classList.remove("btn-primary")
                        button.classList.remove("btn-success")
		            }
		            else {
                        button.classList.add("btn-success")
                        button.classList.remove("btn-primary")
                        button.classList.remove("btn-danger")
                        // Show the close button
                        closebutton.style.visibility = 'visible'
		            }
                }
            });
        } else {
            $.ajax({
                url: '/ajax/user/database/access/close/' + target,
                type: 'get',
                success: function(data) {
                    button.innerText = data
                    button.classList.add("btn-primary")
                    button.classList.remove("btn-success")
                    button.classList.remove("btn-danger")
                    closebutton.style.visibility = 'hidden'
                }
                
            });
        }

    })
})
    
