from app import db
from app.models import User, Message
from flask import url_for, current_app

def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    admin = User.query.filter_by(username='microblog_admin').first()
    with current_app.app_context(), current_app.test_request_context():
        posts_url = url_for('main.get_posts')
    msg = Message(author=admin, recipient=user,
                    body=f'<p>Your posts were successfully exported. <a href={posts_url}>Click to download file</a>')
    db.session.add(msg)
    user.add_notification('unread_message_count', user.new_messages_count())
    db.session.commit()