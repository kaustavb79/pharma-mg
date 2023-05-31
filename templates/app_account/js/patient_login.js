"use strict"

$('#send_otp').click(function(){
    var formData = new FormData();

    formData.append('csrfmiddlewaretoken','{{ csrf_token }}')
    formData.append('mobile',document.getElementsByName('mobile')[0].value)

//    console.log(formData)

    $.ajax({
        type: "POST",
        url: "{% url 'send_otp' %}",// where you wanna post
        data: formData,
        processData: false,
        contentType: false,
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        },
        success: function(data) {
            if(data['status'] === "success"){
                $('#inlineFormInputGroup').attr('readonly','true');
                $('#inlineFormInputGroup').after(
                    `
                    <div class="col-auto my-2 py-2" id="inputOtp">
                        <label class="sr-only" for="inlineFormInputOtpGroup">OTP</label>
                        <div class="input-group mb-2">
                          <div class="input-group-prepend">
                            <div class="input-group-text">OTP</div>
                          </div>
                          <input type="number" name="otp" class="form-control" id="inlineFormInputOtpGroup" minlength="6" required maxlength="6" placeholder="OTP">
                        </div>
                    </div>
                    <button id="button_login" class="w-30 my-3 btn btn-primary" type="submit">Login</button>
                    `
                );
                $('#send_otp').remove();
                $('.NewSignIn_loginFormWrap').prepend(
                    `
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                      OTP sent to your mobile number.
                      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    `
                )
                formSubmit();
            }
            else{
                $('.NewSignIn_loginFormWrap').prepend(
                    `
                    <div class="alert alert-failure alert-dismissible fade show" role="alert">
                      Invalid mobile number.
                      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    `
                )
            }
        }
    });

});


function formSubmit(){
    $('#patient_login_form').on('submit',function(event){
        event.preventDefault();

        var formData = new FormData(document.getElementsByName('patientLoginForm')[0]);
        console.log(formData);

        $.ajax({
        type: "POST",
        url: "{% url 'patient_login' %}",// where you wanna post
        data: formData,
        processData: false,
        contentType: false,
        error: function(jqXHR, textStatus, errorMessage) {
            console.log(errorMessage); // Optional
        },
        success: function(data) {
            if(data['status'] !== "success"){
                $('.NewSignIn_loginFormWrap').prepend(
                    `
                    <div class="alert alert-failure alert-dismissible fade show" role="alert">
                      Invalid OTP < Try Again >.
                      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    `
                )
            }
            else{
                window.location.href = "{% url 'pharmamg:patient_home' %}";
            }
        }
    });

    });
}