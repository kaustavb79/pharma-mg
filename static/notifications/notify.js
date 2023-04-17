var notify_badge_class;
var notify_menu_class;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
// var notify_refresh_period = 50000;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var badges = document.getElementsByClassName(notify_badge_class);
    if (badges) {
        for(var i = 0; i < badges.length; i++){
            badges[i].innerHTML = data.unread_count;
        }
    }
}

function fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        var messages = data.unread_list.map(function (item) {
            var message = "";
            if(typeof item.actor !== 'undefined'){
                message = item.actor;
            }
            if(typeof item.verb !== 'undefined'){
                message = message + " " + item.verb;
            }
            if(typeof item.target !== 'undefined'){
                message = message + " " + item.target;
            }
            if(typeof item.timestamp !== 'undefined'){
                message = message + " " + item.timestamp;
            }
            return '<li>' + message + '</li>';
        }).join('')

        for (var i = 0; i < menus.length; i++){
            menus[i].innerHTML = messages;
        }
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.addEventListener('readystatechange', function(event){
            if (this.readyState === 4){
                if (this.status === 200){
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    registered_functions.forEach(function (func) { func(data); });
                }else{
                    consecutive_misfires++;
                }
            }
        })
        r.open("GET", notify_api_url+'?max='+notify_fetch_count, true);
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data, notify_refresh_period);
    } else {
        var badges = document.getElementsByClassName(notify_badge_class);
        if (badges) {
            for (var i = 0; i < badges.length; i++){
                badges[i].innerHTML = "!";
                badges[i].title = "Connection lost!"
            }
        }
    }
}

// setTimeout(fetch_api_data, 1000);
setTimeout(fetch_api_data, 100000);

// var nf_count = parseInt($('.live_notify_badge').text());
// if (nf_count == 0){
//     $('.badge').addClass('dn');
// }
// else{
//     $('.badge').removeClass('dn');

// }


$(document).ready(function(){
    var notification_count = parseInt($('.live_notification_badge').text());
    if (notification_count != 0){
        $('.notification-counter-div').removeClass('dn');
    }
    else{
        $('.notification-counter-div').addClass('dn');

    }

    var notification_count_message = parseInt($('.live_message_notification_badge').text());
    if (notification_count_message != 0){
        $('.message-counter-div').removeClass('dn');
    }
    else{
        $('.message-counter-div').addClass('dn');

    }

    var notification_count_calendar = parseInt($('.live_calendar_notification_badge').text());
    if (notification_count_calendar != 0){
        $('.calendar-counter-div').removeClass('dn');
    }
    else{
        $('.calendar-counter-div').addClass('dn');
    }

});



