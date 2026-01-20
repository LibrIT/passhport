$(document).ready(function () {
    function sleep(ms) {
          return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Api calls
    async function apicall() {
        addurl = '/ajax/addrm/add/target/user'
        var pathArray = window.location.pathname.split( '/' );
        var targetname = pathArray[pathArray.length -1];
        toadd = document.getElementById('inputadduser').value.split(",")
        var failed = "Error during the process for this users: "

        // Action on items to add
        toadd.map( function(item) {
            $.ajax({
                url: addurl,
                type: 'post',
                data: {"username" : item, "targetname": targetname},
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    bootbox.alert({message:failed + item,
                                   className: "modal modal-danger fade in",
                                  })
                }
            })
        })
        // Refresh datatables on apicall
        await sleep(100)
        $('#attachedusers').DataTable().ajax.reload(null, false);
    }


    // Add when clicking add button
    $(document).on( 'click', '#adduser', function () {
        apicall();
    })  


    // Add when pressing enter
    $('#inputadduser').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            apicall()
        }
    })


    const search = document.getElementById('inputadduser');
    const searchnames = async searchText => {
        const res = await fetch('/ajax/namelist/user');
        const names = await res.json();

        // Match text input
        let matches = names.filter(name => {
            const regex = new RegExp(`${searchText}`, 'gi');
            return name.value.match(regex);
        });

        // Not print all names
        if (searchText.legth === 0) {
            matches = [];
        }

        console.log(matches);
    };
    search.addEventListener('input', () => searchnames(search.value));

});



