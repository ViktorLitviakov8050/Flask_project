function hideTaskInfo(task_id) {
    $('#' + task_id + '-info').remove();
}

$(function() {
    let since = 0;
    setInterval(function() {
        $.ajax(getNotificationsUrl + since).done(
            function(notifications) {
                for (var i = 0; i < notifications.length; i++) {
                        if (notifications[i].name === 'unread_message_count') {
                            console.log('umc');
                            set_message_count(notifications[i].data);
                        }
                        else if (notifications[i].name.includes('task_progress')) {
                            let { progress, task_id } = notifications[i].data;
                            if (progress == 100)
                                hideTaskInfo(task_id);
                            else
                                set_task_progress(
                                    notifications[i].data.task_id,
                                    notifications[i].data.progress);
                        }
                    since = notifications[i].timestamp;
                }
            }
        );
    }, 3000);
});