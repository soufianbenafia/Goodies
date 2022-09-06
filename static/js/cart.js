/**
 * eventlistener test
 */
var updateBtns = document.getElementsByClassName('view-detail')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        console.log('productId:', productId)
    })
}