(function($) {


    function getToken(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getToken('csrftoken')

    /* ..............................................
         Add to Cart send method to cart_add view
         ................................................. */

    $(document).on('click', '.add-button', function(e) {
        e.preventDefault();
        console.log($(this).data("value"))
        console.log($(this).data("qty"))
        $.ajax({
            type: 'POST',
            url: '/add/',
            data: {
                productid: $(this).data("value"),
                qty: $(this).data("qty"),
                csrfmiddlewaretoken: "{{getToken('csrftoken')}}",
                action: 'post'
            },
            success: function(json) {
                document.getElementById("basket-qty").innerHTML = json.qty;
            },
            error: function(xhr, errmsg, err) {}

        });
    })

    $(document).on('click', '.add-button-detail', function(e) {
        e.preventDefault();
        console.log($('#addToCart').val())
        console.log($('#addToCart').data("value"))
        $.ajax({
            type: 'POST',
            url: '/add/',
            data: {
                productid: $('#addToCart').data("value"),
                qty: $('#addToCart').val(),
                csrfmiddlewaretoken: "{{getToken('csrftoken')}}",
                action: 'post'
            },
            success: function(json) {
                document.getElementById("basket-qty").innerHTML = json.qty;
            },
            error: function(xhr, errmsg, err) {}

        });
    })

}(jQuery));