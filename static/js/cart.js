(function($) {

    $('.remove-pr').on('click', function(e) {
        e.preventDefault();
        var prodID = $(this).data("value")
        $.ajax({
            type: 'POST',
            url: '/delete/',
            data: {
                productid: $(this).data("value"),
                csrfmiddlewaretoken: "{{getToken('csrftoken')}}",
                action: 'post'
            },
            success: function(json) {
                $('.delete-itemcart[data-value="' + prodID + '"]').remove();
                document.getElementById("basket-qty").innerHTML = calculateQtySum(json);
                generateCartSide(json)
            },
            error: function(xhr, errmsg, err) {}

        });
    });


    $('.quantity-update').on('input', function(e) {
        e.preventDefault();
        var prodID = $(this).data("value")
        $.ajax({
            type: 'POST',
            url: '/update/',
            data: {
                productid: $(this).data("value"),
                qty: $(this).val(),
                csrfmiddlewaretoken: "{{getToken('csrftoken')}}",
                action: 'post'
            },
            success: function(json) {
                $.each(json, function(key, val) {
                    $.each(JSON.parse(val), function(key, val) {
                        if (key == prodID) {
                            $.each(val, function(key, val) {
                                if (key == "total_price") {
                                    var total_price = `${val}`
                                    $('.total-prp[data-index="' + prodID + '"]').text(total_price);
                                }
                            });
                        }
                    });
                });
                var subTotal = calculateSubTotal(json)
                var tax = calculateTax(json)
                    //var ship = getShippingCosts(subTotal, tax)
                var grandTotal = parseFloat(parseFloat(subTotal) + parseFloat(tax)).toFixed(2)

                console.log("subTotal: " + subTotal)
                console.log("tax: " + tax)
                console.log("grandTotal: " + grandTotal)

                $('.sub-total-update').text("€ " + subTotal);
                $('.tax-update').text("€ " + tax);
                $('.grandTotal-update').text("€ " + grandTotal);
                document.getElementById("basket-qty").innerHTML = calculateQtySum(json);
                generateCartSide(json)
            },
            error: function(xhr, errmsg, err) {}

        });
    });


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
                document.getElementById("basket-qty").innerHTML = calculateQtySum(json);
                generateCartSide(json)
            },

            error: function(xhr, errmsg, err) {}

        });
    })

    $(document).on('click', '.add-button-detail', function(e) {
        e.preventDefault();
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
                document.getElementById("basket-qty").innerHTML = calculateQtySum(json);
                generateCartSide(json)
            },
            error: function(xhr, errmsg, err) {}

        });
    })


    function getShippingCosts(subtotal, tax) {
        var subTotalTax = parseFloat(subtotal + tax).toFixed(2)
        var amountFixedShip = 49
        if (subTotalTax < amountFixedShip) {
            return 4.99
        } else {
            return 0
        }
    }

    function calculateTax(json) {
        var subTotal = calculateSubTotal(json)
        return parseFloat((subTotal / 100) * 7).toFixed(2);
    }

    function calculateSubTotal(json) {
        var total = 0;
        $.each(json, function(key, val) {
            $.each(JSON.parse(val), function(key, val) {
                $.each(val, function(key, val) {
                    if (key == "total_price") {
                        var total_price = `${val}`
                        total += parseFloat(total_price);

                    }
                });
            });
        });
        return parseFloat(total).toFixed(2);
    }

    function calculateQtySum(json) {
        var qtySum = 0;
        $.each(json, function(key, val) {
            $.each(JSON.parse(val), function(key, val) {
                $.each(val, function(key, val) {
                    if (key == "qty") {
                        qty = `${val}`
                        qtySum = qtySum + parseInt(qty);
                    }
                });
            });
        });
        return qtySum.toString();
    }

    function generateCartSide(json) {
        var cartBox = $('li.cart-box');
        cartBox.empty()
        var ul;
        $.each(json, function(key, val) {
            $.each(JSON.parse(val), function(key, val) {
                ul = $("<ul></ul>")
                ul.addClass('cart-list')
                cartBox.append(ul)

                var li = $("<li></li>")
                ul.append(li)

                var a = $("<a></a>")
                a.addClass('photo')
                li.append(a)

                var img = $('<img id="dynamic">');
                img.addClass('cart-thumb')
                a.append(img)

                var h6 = $("<h6></h6>")
                var h6_a = $("<a></a>")
                h6.append(h6_a)
                li.append(h6)

                var p = $("<p></p>")
                var p_span = $("<span></span>")
                p_span.addClass('price')
                li.append(p)

                var qty;
                $.each(val, function(key, val) {
                    if (key == "image") {
                        img.attr('src', `${val}`);
                    }
                    if (key == "name") {
                        h6_a.text(`${val}`);
                    }
                    if (key == "qty" || key == "total_price") {
                        if (key == "qty") {
                            qty = `${val}`
                        }

                        if (key == "total_price") {
                            p.html(qty + "  - " + '<span class="price">' + `${val}` + '</span>');
                        }
                    }
                });
            });
        });
        var liTotal = $("<li></li>")
        liTotal.addClass('total')
        ul.append(liTotal)
        var aTotal = $("<a></a>")
        aTotal.addClass('btn btn-default hvr-hover btn-cart')
        aTotal.attr("href", "/cart.html/")
        aTotal.text('VIEW CART')
        liTotal.append(aTotal)

        var spanTotal = $("<span></span>")
        spanTotal.addClass('float-right')
        liTotal.append(spanTotal)
        spanTotal.html('<strong>' + "Total: " + '</strong>' + calculateSubTotal(json));
    }


    $(window).on("popstate", function(event) {
        console.log("digga")
    });
}(jQuery));