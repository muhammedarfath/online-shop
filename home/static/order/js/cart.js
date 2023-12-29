
document.addEventListener('DOMContentLoaded', function() {
$('.changequantity').off('click').click(function(e) {
    e.preventDefault();
    var action = $(this).data('action');
    var productId = $(this).data('product-id');
    var input = $('#product_qty' + productId);
    var qty = parseInt(input.val(), 10) || 0;
    console.log(action)
    console.log(productId)
    if (action === 'increment') {
        qty += 1;
    } else if (action === 'decrement' && qty > 0) {
        qty -= 1;
    }

    $.ajax({
        method: "POST",
        url: "/update_quantity/",
        data: {
            'product_id': productId,
            'quantity': qty,
            'action': action,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
            single_price = response.single_price;
            if (response.status === 'Requested quantity exceeds available quantity') {
                Swal.fire({
                    icon: "error",
                    title: "Requested quantity exceeds available quantity",  // Display the message text as the title
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                      toast.addEventListener("mouseenter", Swal.stopTimer);
                      toast.addEventListener("mouseleave", Swal.resumeTimer);
                    }
                  });

            } else if (response.status === 'Zero quantity not allowed' || response.status === 'Invalid request method') {
                Swal.fire({
                    icon: "error",
                    title: "Zero quantity not allowed",  // Display the message text as the title
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                      toast.addEventListener("mouseenter", Swal.stopTimer);
                      toast.addEventListener("mouseleave", Swal.resumeTimer);
                    }
                  });
            } else {
                // Update single price and grand total
                if (qty === 0) {
                    // If the quantity becomes zero, set it to 1
                    qty = 1;
                }

                // Update the quantity in the text field
                input.val(qty);

                // Update single price and grand total
                document.getElementById('singlePriceDisplay' + productId).textContent = response.single_price;
                $('#grandTotalDisplay').text(response.grand_total);
                $('#taxDisplay').text( response.tax);
                $('#shippingDisplay').text(response.shipping);
                $('#totalDisplay').text(response.total);
                console.log("Single Price:", response.single_price);
                console.log("Tax:", response.tax);
                console.log("Shipping:", response.shipping);
            }
        },
        error: function(error) {
            alert("Error updating cart.");
        }
    });
});
});
