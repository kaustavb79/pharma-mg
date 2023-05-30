"use strict"

$(function(){
  $('#datepicker').datepicker();
});

$('#appointment_form').on('submit',function(event){
    event.preventDefault();

    var formData = new FormData(document.getElementsByName('createAppointmentForm')[0]);
    console.log(formData)

    $.ajax({
        type: "POST",
        url: "{% url 'pharmamg:schedule_consultation_ajax' %}",// where you wanna post
        data: formData,
        processData: false,
        contentType: false,
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        },
        success: function(data) {
            alert(data['messsage'])
        }
    });
});