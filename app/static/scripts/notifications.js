$(function() {
    let since = 0;
    setInterval(function() {
        $.ajax(getNotificationsUrl + since).done(
            function(notifications) {
                for (var i = 0; i < notifications.length; i++) {
                    switch (notifications[i].name) {
                        case 'unread_message_count':
                            set_message_count(notifications[i].data);
                            break;
                        case 'task_progress':
                            set_task_progress(
                                notifications[i].data.task_id,
                                notifications[i].data.progress);
                            break;
                    }
                    since = notifications[i].timestamp;
                }
            }
        );
    }, 3000);
});