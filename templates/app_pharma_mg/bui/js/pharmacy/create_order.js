"use strict"

$(document).ready(function() {
    $('.js-example-basic-single').select2();
});


$('#order_form').on('submit',function(event){
    event.preventDefault();

    var formData = new FormData(document.getElementsByName('createOrderForm')[0]);
    console.log(formData)

    $.ajax({
        type: "POST",
        url: "{% url 'pharmamg:create_order_ajax' %}",// where you wanna post
        data: formData,
        processData: false,
        contentType: false,
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        },
        success: function(data) {
            $('.btn-close').click();
            location.reload();
        }
    });

});