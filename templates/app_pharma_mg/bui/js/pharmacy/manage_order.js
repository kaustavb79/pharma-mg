"use strict"


$('.editForm').on('submit',function(event){
    event.preventDefault();

    var formData = new FormData(document.getElementsByName('editProductForm')[0]);
    formData.append('item_id', document.getElementById('id_item_id').value);
    console.log(formData)
    $.ajax({
        type: "POST",
        url: "{% url 'pharmamg:edit_product_form_ajax' %}",// where you wanna post
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