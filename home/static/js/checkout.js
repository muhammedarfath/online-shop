$(document).ready(function (){
    $('.paywithrazorpay').click(function(e){
        e.preventDefault();

        var fname =$("[name='first_name']").val();
        var lname =$("[name='last_name']").val();
        var email =$("[name='email']").val();
        var number =$("[name='phone']").val();
        var address =$("[name='address_line1']").val();
        var city =$("[name='city']").val();
        var state =$("[name='state']").val();
        var pin =$("[name='contry']").val();
        var token =$("[name='csrfmiddlewaretoken']").val();


       if (fname == "" || lname == "" || email == "" || number == "" || address == "" || city == "" || state == "" || pin == "")
       {
        Swal.fire('Alert!',"All fields are mandatory!","error");
        return false;
       }
       else{
        $.ajax({
            method:"GET",
            url:"/proceed-to-pay/",
            success:function(response){
                console.log(response);

            var options = {
                "key": "rzp_test_jZl2ZJHfu0FLqr", // Enter the Key ID generated from the Dashboard
                "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Coloshop", //your business name
                "description": "Thank you for buying from us",
                "image": "https://example.com/your_logo",
                // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (response){
                    alert(response.razorpay_payment_id);
                    data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone": phone,
                        "address_line1": address_line1,
                        "city": city,
                        "state": state,
                        "contry": contry,
                        "payment_mode": "Paid by Razorpay",
                        "payment_id": response.razorpay_payment_id,
                        csrfmiddlewaretoken: token
                    }
                    
                    $.ajax({
                        method:"POST",
                        url:"/payment/",
                        data:data,
                        success:function(response){
                            Swal.fire('Congratulations!',response.status,"success").then((value) => {
                                window.location.href = '/my-orders/'
                            });
                        
                        }
                    });

                
                },
                // "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                //     "name": fname+" "+lname, //your customer's name
                //     "email": email, 
                //     "contact": number,  //Provide the customer's phone number for better conversion rates 
                // },
                "theme": {
                    "color": "#3399cc"
                }
            };
        var rzp1 = new Razorpay(options);

        rzp1.open();
       }
 

    })
}
});
})

