// tooltip mouseover
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();   
});

//Flash message fade out
$(document).ready(function(){
    setTimeout(function() {
        $('#flashmessage').fadeOut('fast');
    }, 10000); // <-- time in milliseconds
});
