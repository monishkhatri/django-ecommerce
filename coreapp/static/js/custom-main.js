function amount(value){
    return value.toLocaleString('en-US')
}
function updateCartBag(value){
    $(".shoppingBag").html(value)
}
$(document).ready(function(){
    /*------------------------Cart Code Start-----------------------*/
    /*------------------------------------------------------------*/
    
    function cartOperation(productId, productQty = 1, type="add"){

        url = '/my-cart/add/' + productId + "/";
        alertMessage = "Item added to your bag";
        confirmTxt = "Visit My Cart";
        cancelButton = true        
        if(type == "remove"){
            url = '/my-cart/clearitem/' + productId + "/";
            alertMessage = "Item removed from your bag";
            confirmTxt = "Okay";
            cancelButton = false
        } else if (type == "increment"){
            url = '/my-cart/add/' + productId + "/";
            alertMessage = "Item Quantity has been updated";
            confirmTxt = "Okay";
            cancelButton = false
        } else if (type == "decrement"){
            url = '/my-cart/remove/' + productId + "/";
            alertMessage = "Item Quantity has been updated";
            confirmTxt = "Okay";
            cancelButton = false
        }
        
        $.ajax({
            type : 'POST',
            dataType: 'json',
            url : url,
            data : {
                productId : productId,
                cartQty : productQty
            },
            success : function(response) {
                Swal.fire({
                    icon: 'success',
                    title: alertMessage,
                    confirmButtonText: confirmTxt,
                    showCancelButton: cancelButton,
                    cancelButtonText: 'Continue Shopping'
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location = "/my-cart";
                    }
                })
            }
        });
    }

    $(".qtybtn").click(function(){
        if ($(this).hasClass('inc')) {
            product = $(this).prev().data('proid')
            cartOperation(product, 1, "increment");
        } else {
            product = $(this).next().data('proid')
            cartOperation(product, 1, "decrement");
        }
    })
    
    $( ".add-to-cart" ).click(function() {
        product = $(this).data("proid");
        productQty = $(".cartQty").val();
        cartOperation(product, productQty);
    });
    $( ".clear-cart" ).click(function() {
        product = $(this).data("proid");
        Swal.fire({
            icon: 'warning',
            title: 'Are you sure you want to remove from cart',
            showCancelButton: true,
            confirmButtonText: 'Yes',
            denyButtonText: 'NO its by mistake',
        }).then((result) => {
            if (result.isConfirmed) {
                cartOperation(product, 0, "remove");
            }
        })
    });
    /*------------------------------------------------------------*/
    /*------------------------Cart Code End-----------------------*/
})
