(function($) {
    $(".dataChanger").on('change', function() {
        var selected = $(this).find(":selected").val();
        console.log(selected)
        if (selected === '/register.html/') {
            window.location.href = '/register.html/';
        } else if (selected === '/login/') {
            window.location.href = '/login/';
        }
    })

    $("input[type=radio][name=deliveryOption]").on("change", function(e) {
        e.preventDefault();
        console.log("trigger yes");
        $.ajax({
            type: "POST",
            url: 'basket_update_delivery',
            data: {
                deliveryoption: $(this).val(),
                action: "post",
            },
            success: function(json) {
                document.getElementById("total").innerHTML = json.total;
                document.getElementById("delivery_price").innerHTML = json.delivery_price;
            },
            error: function(xhr, errmsg, err) {},
        });
    });
}(jQuery));