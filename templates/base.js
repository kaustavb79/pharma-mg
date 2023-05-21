"use strict"
{% load static %}

function googleTranslateElementInit() {
  new google.translate.TranslateElement({
  pageLanguage: 'en'
  }, 'google_translate_element');
}

function google_translate_element_btn(){
    if($(".google_translate_element_btn").hasClass('o')){
        close_google_translate();
    }else{
        open_google_translate();
    }
}
function open_google_translate(){
    $("#google_translate_element").removeClass('dn');
    $(".google_translate_element_btn").addClass('o');

    $(document).bind('click.google_translate',function(e){
        var container = $("#google_translate_element");
        var container2 = $(".google_translate_element_btn");
//                console.log(e);
        // if the target of the click isn't the container nor a descendant of the container
        if ((!container.is(e.target) && container.has(e.target).length === 0)&&
        (!container2.is(e.target) && container2.has(e.target).length === 0))
        {
            close_google_translate();
            $(document).unbind('click.google_translate');
        }
    });
}
function close_google_translate(){
    $("#google_translate_element").addClass('dn');
    $(".google_translate_element_btn").removeClass('o');
}



/*
    network status
*/
function checkNetworkStatus(){
    function hasNetwork(online) {
      const element = document.querySelector(".app_status");
      // Update the DOM to reflect the current status
      if (online) {
        if(element.classList.contains('offline')){
            element.classList.remove("offline");
            element.classList.add("online");
            element.innerText = "You are back online";
//            element.animate({
//                opacity: "-=1"
//            }, 1000, function() {
//                element.remove();
//            });

            $(element).fadeOut(3000)
        }
      } else {
        element.classList.remove("online");
        element.classList.add("offline");
        element.innerText = "You are offline";
        $(element).fadeIn(500)
      }
    }

    window.addEventListener("load", () => {
          hasNetwork(navigator.onLine);

          window.addEventListener("online", () => {
            // Set hasNetwork to online when they change to online.
            hasNetwork(true);
          });

          window.addEventListener("offline", () => {
            // Set hasNetwork to offline when they change to offline.
            hasNetwork(false);
          });

    });
}



// DRIVER SEGMENT [METHOD CALLS]
$(document).ready(function(){
    $(".google_translate_element_btn").unbind("click.google_translate_element_btn", google_translate_element_btn)
    $(".google_translate_element_btn").bind("click.google_translate_element_btn", google_translate_element_btn)

    googleTranslateElementInit();
    $("body").on("change", "#google_translate_element select", function (e) {
        console.warn(e);
        console.warn($(this).find(":selected").text());
        console.warn($(this).find(":selected").val());
        google_translate_element_btn();
    });

    checkNetworkStatus();

});




