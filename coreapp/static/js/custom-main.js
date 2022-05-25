function loadShoppingBagCounter(){
    cartData = JSON.parse(localStorage.getItem('cartData'))
    len = Object.keys(cartData).length
    
    $(".shoppingBag").html(len)
}

$(document).ready(function(){
    
    /*------------------------Cart Code Start-----------------------*/
    if (localStorage.getItem('cartData') == null){
        var cartData = {};
    } else {
        cartData = JSON.parse(localStorage.getItem('cartData'))
    }
    loadShoppingBagCounter()
    /*------------------------Cart Code End-----------------------*/

    $( ".add-to-cart" ).click(function() {
        dataSlug = $(this).data("slug")
        cartQty = $(".cartQty").val()
        if (cartData[dataSlug] !== undefined){
            cartData[dataSlug] = parseInt(cartData[dataSlug]) + parseInt(cartQty)
        } else {
            cartData[dataSlug] = parseInt(cartQty)
        }
        localStorage.setItem('cartData', JSON.stringify(cartData))
        loadShoppingBagCounter()
    });
})
