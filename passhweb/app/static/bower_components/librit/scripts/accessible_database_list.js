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
        'ajax'        : {
            url     : '/ajax/user/database/list',
            dataSrc : 'data'
        }
    })
    
    // Pushing the askbutton open a connexion for user IP
    $('tbody').on( 'click', '#accessask', function () {
        button = this
        firstcell = $(this).parents('tr').children('td')[0]
        target = firstcell.innerText

        // First time we press the button, we open a connection
        if(button.classList.contains("btn-primary")) {
            $.ajax({
                url: '/ajax/user/database/access/' + target,
                type: 'get',
                success: function(data) {
                    button.innerText = data
                    button.classList.add("btn-success")
                    button.classList.remove("btn-primary")
                }
            });
        }

    } )
})
    
