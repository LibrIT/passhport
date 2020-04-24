$(document).ready(function () {
    // enhance checkbox
    //Flat red color scheme for iCheck
    $('input[type="checkbox"].flat-blue, input[type="radio"].flat-blue').iCheck({
        checkboxClass: 'icheckbox_flat-blue',
        radioClass   : 'iradio_flat-blue',
        //increaseArea: '20%' // optional
    });
    

    // Remove/add additionnal infos for SSH targets (login, port, options)
    var type = $('#targettype').val();
    if (type != "ssh") {
        othertype()
    }
    else {
        sshtype()
    }
})

// Refresh the form fields if we change the type
$(document).on('change', '#targettype', function(){
    var type = $('#targettype').val();
    if (type != "ssh") {
        othertype()
    }
    else {
        sshtype()
    }
})

function othertype() {
    // hide useless form inputs
    $('#login').parent().hide();
    $('#options').parent().hide();
    $('#changepwd').parent().hide();
    $('#sessiondur').parent().show();
    // Remove useless br
    $('#login').parent().next('br').hide();
    if  ($('#targettype').val() == "mysql") {
        $('#port').attr('placeholder','Port (default is 3306)');
    }
    else {
        if  ($('#targettype').val() == "postgresql") {
            $('#port').attr('placeholder','Port (default is 5432)');
        }
        else { //Oracle
            $('#port').attr('placeholder','Port (default is 1521)');
        }
    }
    $('#sessiondur').parent().next('br').show();
    $('#options').parent().next('br').hide();
    $('#changepwd').parent().next('br').hide();
}

function sshtype() {
    //show form inputs
    $('#login').parent().show();
    $('#options').parent().show();
    $('#changepwd').parent().show();
    $('#port').attr('placeholder','Port (default is 22)');
    $('#options').parent().next('br').show();
    $('#changepwd').parent().next('br').show();
    $('#sessiondur').parent().hide();
    $('#sessiondur').parent().next('br').hide();
}
