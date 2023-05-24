"use strict"

$('.editForm').on('submit',function(event){
    event.preventDefault();

    var formData = new FormData(document.getElementsByName('editForm')[0]);
    console.log(formData)
    $.ajax({
        type: "POST",
        url: "{% url 'pharmamg:edit_form_ajax' %}",// where you wanna post
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
