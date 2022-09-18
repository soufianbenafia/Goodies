(function($) {
    $(".dataChanger").on('change', function() {
        var selected = $(this).find(":selected").val();
        console.log(selected)
        if (selected === '/register.html/') {
            window.location.href = '/register.html/';
        } else if (selected === '/my-account.html/') {
            window.location.href = '/my-account.html/';
        }
    })
}(jQuery));