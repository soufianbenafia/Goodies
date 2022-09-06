/**
 * eventlistener test
 */
var updateBtns = document.getElementsByClassName('view-detail')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

        updateShopDetail(productId, action)

    })

    function updateShopDetail(productId, action) {
        console.log('User is authenticated, sending data...')

        var url = '/shop-detail.html/'

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })

        .then((data) => {
            location.reload()
        });
    }
}